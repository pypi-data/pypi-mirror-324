import glob
import os
import subprocess
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse
from uuid import uuid4

import requests
from google.api_core.exceptions import Forbidden, NotFound
from google.cloud import storage
from loguru import logger

from earthscale.auth import get_supabase_client
from earthscale.constants import BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL
from earthscale.datasets.dataset import Dataset
from earthscale.datasets.raster import (
    EarthEngineDataset,
    ImageDataset,
    TileServerDataset,
    ZarrDataset,
)
from earthscale.datasets.vector import VectorDataset


class UnsupportedDatasetType(Exception):
    pass


class UnsupportedPathProtocol(Exception):
    pass


INGESTABLE_DATASET_TYPES = (
    ImageDataset,
    VectorDataset,
    ZarrDataset,
)

ALWAYS_READABLE_DATASET_TYPES = (
    EarthEngineDataset,
    TileServerDataset,
)


def validate_if_dataset_is_ingestable(dataset: Dataset[Any]) -> None:
    """Validate that we can ingest this dataset into our shared storage."""
    if isinstance(dataset, ALWAYS_READABLE_DATASET_TYPES):
        return
    if not isinstance(dataset, INGESTABLE_DATASET_TYPES):
        raise UnsupportedDatasetType(
            f"Sorry, we do not yet support ingesting datasets of type: {type(dataset)}."
        )

    # Check whether path protocol is supported
    urls = _get_dataset_source_urls(dataset)
    for url in urls:
        protocol = urlparse(url).scheme
        if protocol not in ("gs",):
            raise UnsupportedPathProtocol(
                "Sorry, we do not yet support ingesting datasets with the "
                f"{protocol} protocol."
            )


def _get_dataset_source_urls(dataset: Dataset[Any]) -> list[str]:
    if isinstance(dataset, ImageDataset):
        return (
            [dataset.definition.glob_url]
            if isinstance(dataset.definition.glob_url, str)
            else dataset.definition.glob_url
        )
    elif isinstance(dataset, ZarrDataset):
        return [str(dataset._store)]
    elif isinstance(dataset, VectorDataset):
        return [dataset.url]
    else:
        raise UnsupportedDatasetType(f"Unsupported dataset type: {type(dataset)}")


def is_path_readable(path: str, client: storage.Client) -> bool:
    parsed_url = urlparse(path)
    is_local_url = parsed_url.scheme == "" or parsed_url.scheme == "file"
    if is_local_url:  # Also try local ls as fallback
        # Need to use glob.glob() for wildcard paths since ls doesn't handle them
        if parsed_url.scheme == "file":
            path = path.replace("file://", "")
        matching_files = glob.glob(path)
        local_result = len(matching_files) > 0
        return local_result

    if parsed_url.scheme != "gs":
        return False

    bucket_name = parsed_url.netloc
    blob_name = parsed_url.path.lstrip("/")
    try:
        bucket = client.bucket(bucket_name)

        # First, try glob match
        glob_blobs = list(bucket.list_blobs(match_glob=blob_name, max_results=1))
        if len(glob_blobs) > 0:
            return True

        # Next, assume it's a directory and try glob match for blobs in the directory
        match_glob = str(Path(blob_name) / "*")
        blobs = list(bucket.list_blobs(match_glob=match_glob, max_results=1))
        if len(blobs) > 0:
            return True
    except (NotFound, Forbidden):
        return False

    return False


def is_dataset_readable_by_earthscale(dataset: Dataset[Any]) -> bool:
    if isinstance(dataset, ALWAYS_READABLE_DATASET_TYPES):
        return True
    backend_url = os.getenv(BACKEND_URL_ENV_VAR, DEFAULT_BACKEND_URL).rstrip("/")
    client = get_supabase_client()
    urls = _get_dataset_source_urls(dataset)
    for url in urls:
        response = requests.get(
            f"{backend_url}/ingest/has-read-access",
            params={"path": url},
            headers={
                "Authorization": f"Bearer {client.auth.get_session().access_token}"
            },
        )
        response.raise_for_status()
        can_read = cast(bool, response.json())
        if not can_read:
            return False
    return True


def _get_shared_bucket() -> str:
    client = get_supabase_client()
    # Get the user's organization ID by joining users table
    user_id = client.auth.get_user().user.id
    result = client.from_("users").select("org_id").eq("id", user_id).limit(1).execute()
    if len(result.data) == 0:
        raise ValueError("Could not find organization for user")
    org_id = result.data[0]["org_id"]

    # Get the shared bucket path for this org
    result = (
        client.from_("shared_buckets")
        .select("bucket_path")
        .eq("org_id", org_id)
        .limit(1)
        .execute()
    )
    if len(result.data) == 0:
        raise ValueError("Could not find shared bucket for organization")

    bucket = cast(str, result.data[0]["bucket_path"])
    # Add subdir for ingested data
    bucket = os.path.join(bucket, "earthscale_ingest_output")
    return bucket


def _get_base_gcloud_cmd() -> list[str]:
    """Get base gcloud command"""
    return [
        "gcloud",
        "storage",
    ]


def _ingest_image_dataset(dataset: ImageDataset, shared_bucket: str) -> Dataset[Any]:
    # Get list of files matching glob pattern

    # Run gsutil ls to get list of files
    ingest_urls = (
        [dataset.definition.glob_url]
        if isinstance(dataset.definition.glob_url, str)
        else dataset.definition.glob_url
    )
    dest_dir = os.path.join(shared_bucket, str(uuid4()), "")
    for ingest_url in ingest_urls:
        cmd = [*_get_base_gcloud_cmd(), "ls", ingest_url]
        ls_result = subprocess.run(cmd, capture_output=True, text=True)
        if ls_result.returncode != 0:
            raise RuntimeError(f"Failed to list files: {ls_result.stderr}")

        source_files = ls_result.stdout.splitlines()

        # Create destination directory in shared bucket (ensure there is a trailing
        # slash)
        logger.info(
            f"Copying {len(source_files)} files from {ingest_url} to " f"{dest_dir}"
        )

        # Use gsutil -m cp -I for parallel copy
        source_files_bytes = "\n".join(source_files).encode()
        cp_cmd = [*_get_base_gcloud_cmd(), "cp", "-I", str(dest_dir)]
        cp_result = subprocess.run(
            cp_cmd, input=source_files_bytes, capture_output=True
        )
        if cp_result.returncode != 0:
            raise RuntimeError(f"Failed to copy files: {cp_result.stderr.decode()}")

    # Return new dataset pointing to copied files
    return ImageDataset(
        glob_url=os.path.join(dest_dir, "*"),
        bands=dataset.definition.bands,
        band_info=dataset.definition.band_info,
        groupby=dataset.definition.groupby,
        datetime_=dataset.definition.datetime_,
        filename_date_pattern=dataset.definition.filename_date_pattern,
        name=dataset.name,
        metadata=dataset.metadata,
        **dataset.definition.kw_args,
    )


def _ingest_vector_dataset(dataset: VectorDataset, shared_bucket: str) -> Dataset[Any]:
    # Create destination directory in shared bucket
    dest_dir = os.path.join(shared_bucket, str(uuid4()))
    # Get filename from source url
    src_filename = os.path.basename(dataset.url)
    dest_path = os.path.join(dest_dir, src_filename)
    logger.info(f"Copying {dataset.url} to {dest_path}")

    # Use gsutil cp to copy file
    cp_cmd = [*_get_base_gcloud_cmd(), "cp", dataset.url, str(dest_path)]
    cp_result = subprocess.run(cp_cmd, capture_output=True)
    if cp_result.returncode != 0:
        raise RuntimeError(f"Failed to copy file: {cp_result.stderr.decode()}")

    # Return new dataset pointing to copied file
    return VectorDataset(
        url=str(dest_path),
        name=dataset.name,
        metadata=dataset.metadata,
        start_date_field=dataset.start_date_field,
        end_date_field=dataset.end_date_field,
    )


def _ingest_zarr_dataset(dataset: ZarrDataset, shared_bucket: str) -> Dataset[Any]:
    store = dataset._store
    # Create destination directory in shared bucket
    base = os.path.basename(store)
    dest_dir = os.path.join(shared_bucket, str(uuid4()), base)
    logger.info(f"Copying {store} to {dest_dir}")

    # Use gcloud cp -R for parallel recursive copy of zarr store
    cp_cmd = [*_get_base_gcloud_cmd(), "cp", "-R", str(store), str(dest_dir)]
    cp_result = subprocess.run(cp_cmd, capture_output=True)
    if cp_result.returncode != 0:
        raise RuntimeError(f"Failed to copy zarr store: {cp_result.stderr.decode()}")

    # Return new dataset pointing to copied store
    return ZarrDataset(
        store=dest_dir,
        name=dataset.name,
        metadata=dataset.metadata,
        rename=dataset._rename,
        **dataset._kwargs,
    )


def ingest_dataset_to_earthscale(dataset: Dataset[Any]) -> Dataset[Any]:
    """
    Ingest a dataset into Earthscale's shared storage. Return the dataset
    definition that can be used to register the dataset.

    """
    shared_bucket = _get_shared_bucket()
    if isinstance(dataset, ImageDataset):
        return _ingest_image_dataset(dataset, shared_bucket)
    elif isinstance(dataset, VectorDataset):
        return _ingest_vector_dataset(dataset, shared_bucket)
    elif isinstance(dataset, ZarrDataset):
        return _ingest_zarr_dataset(dataset, shared_bucket)
    else:
        raise UnsupportedDatasetType(
            f"We do not yet support ingesting {type(dataset)}."
        )
