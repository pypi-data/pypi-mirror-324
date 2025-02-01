import functools
import uuid
from pathlib import Path
from typing import cast

import fsspec
import rasterio
from pyogrio import read_info
from rasterio.crs import CRSError
from rasterio.warp import transform_bounds
from shapely import MultiPolygon
from shapely.geometry import box

from earthscale.auth import get_fsspec_storage_options
from earthscale.datasets.dataset import (
    Dataset,
    DatasetDefinition,
    DatasetMetadata,
    DatasetStatus,
    DatasetType,
    DimensionInfo,
    registry,
)
from earthscale.google_cloud_utils import get_region_from_gcs_url
from earthscale.utils import create_valid_url, is_gcs_url

_DEFAULT_VECTOR_BAND = "default"


@functools.lru_cache
def _get_bounds(url: str) -> tuple[float, float, float, float]:
    extra_options = get_fsspec_storage_options(url)
    fs, _ = fsspec.url_to_fs(url, **extra_options)
    if not fs.exists(url):
        raise FileNotFoundError(f"File {url} does not exist.")
    with fs.open(url) as f:
        info = read_info(f, force_total_bounds=True)
    total_bounds: tuple[float, float, float, float] = info["total_bounds"]

    crs = rasterio.CRS.from_user_input(info["crs"])
    try:
        epsg = crs.to_epsg()
    except CRSError:
        epsg = None

    if epsg is None or epsg != 4326:
        crs_4326 = rasterio.CRS.from_epsg(4326)
        total_bounds = cast(
            tuple[float, float, float, float],
            transform_bounds(
                crs,
                crs_4326,
                *total_bounds,
            ),
        )
    return total_bounds


class VectorDatasetDefinition(DatasetDefinition):
    url: str
    start_date_field: str | None
    end_date_field: str | None


class VectorDataset(Dataset[VectorDatasetDefinition]):
    """Dataset based on vector file

    Args:
        url:
            URL of the vector file
        name:
            Name of the dataset as shown in the platform
    """

    def __init__(
        self,
        url: str | Path,
        name: str | None = None,
        metadata: DatasetMetadata | None = None,
        attributes: dict[str, str] | None = None,
        start_date_field: str | None = None,
        end_date_field: str | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
    ):
        # HACK: As we're re-writing the visualization logic, a vector dataset will just
        #       define a "default" visualization. Later-on users will be able to style
        #       the vector layer in the frontend.
        # TODO: do similar checks for value_map and colormap
        # if metadata is not None and len(metadata.visualizations) > 0:
        #     raise ValueError(
        #         "Vector datasets cannot have custom visualizations at the moment"
        #     )
        metadata = metadata or DatasetMetadata()

        explicit_name = name is not None
        name = name or str(uuid.uuid4())
        url = create_valid_url(str(url))
        self.url = url
        self.start_date_field = start_date_field
        self.end_date_field = end_date_field

        definition = VectorDatasetDefinition(
            url=str(url),
            start_date_field=start_date_field,
            end_date_field=end_date_field,
        )

        super().__init__(
            name,
            explicit_name,
            attributes,
            metadata,
            type_=DatasetType.VECTOR,
            status=DatasetStatus.NOT_STARTED,
            definition=definition,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    def get_extent(self) -> MultiPolygon:
        return MultiPolygon([box(*_get_bounds(str(self.url)))])

    @property
    def data_region(self) -> str | None:
        if is_gcs_url(self.url):
            return get_region_from_gcs_url(self.url)
        return None

    def get_dimension_info(self) -> DimensionInfo:
        return DimensionInfo(dimensions=[], band_dimensions=[])

    def get_uncompressed_size_bytes(self) -> int:
        # TODO: for now, vector datasets are free :)
        return 0


registry.register_class("VectorDataset", VectorDataset)
