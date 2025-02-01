import concurrent
import datetime
import glob
import uuid
from collections.abc import Hashable, Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from copy import copy
from pathlib import Path
from typing import Any, cast

import fsspec
import numpy as np
import pandas as pd
import xarray as xr
from loguru import logger
from odc.geo import BoundingBox
from odc.geo._xr_interop import spatial_dims, xr_coords, xr_reproject
from odc.geo.geobox import GeoBox
from pyproj import CRS
from rio_tiler.constants import WGS84_CRS

from earthscale.auth import get_fsspec_storage_options
from earthscale.datasets.dataset import (
    DatasetDefinition,
    DatasetMetadata,
    DimensionInfo,
)
from earthscale.datasets.graph import create_source_graph
from earthscale.datasets.raster import (
    RasterDataset,
)
from earthscale.datasets.raster._base import get_dimensions_from_dataset
from earthscale.exceptions import (
    MemoryLimitExceededError,
    NoDataInSelectionError,
    NoFilesForGlobError,
)
from earthscale.google_cloud_utils import get_region_from_gcs_url
from earthscale.odc_geo_extensions import (
    clip_geobox,
    compute_output_geobox_without_buffering,
)
from earthscale.raster_utils import (
    find_latitude_dimension,
    find_longitude_dimension,
    find_x_dimension,
    find_y_dimension,
)
from earthscale.types import BBOX, Chunksizes
from earthscale.utils import is_gcs_url, parse_dimension_placeholder_path, utc_datetime

_WEB_MERCATOR_BBOX = BoundingBox(
    -20037508.342789244,
    -20037508.342789244,
    20037508.342789244,
    20037508.342789244,
    "EPSG:3857",
)


def _crs_from_attrs(xr_attrs: dict[Hashable, Any]) -> CRS | None:
    # Logic as described here:
    # https://gdal.org/en/latest/drivers/raster/zarr.html#srs-encoding
    # https://gdal.org/en/latest/drivers/raster/netcdf.html#georeference
    # https://corteva.github.io/rioxarray/latest/getting_started/crs_management.html
    with suppress(KeyError, TypeError):
        return CRS.from_user_input(xr_attrs["_CRS"]["url"])

    with suppress(KeyError, TypeError):
        return CRS.from_wkt(xr_attrs["_CRS"]["wkt"])

    with suppress(KeyError, TypeError):
        return CRS.from_json_dict(xr_attrs["_CRS"]["projjson"])

    with suppress(KeyError, TypeError):
        return CRS.from_wkt(xr_attrs["spatial_ref"]["crs_wkt"])

    with suppress(KeyError, TypeError):
        return CRS.from_wkt(xr_attrs["spatial_ref"])

    return None


def _detect_zarr_crs(dset: xr.Dataset) -> CRS | None:
    crs = _crs_from_attrs(dset.attrs)
    if crs is not None:
        return crs
    with suppress(KeyError, TypeError):
        crs = _crs_from_attrs(dset["spatial_ref"].attrs)
        if crs is not None:
            return crs

    array_crs: dict[Hashable, CRS] = {}
    for array_name in dset:
        array = dset[array_name]
        current_crs = _crs_from_attrs(array.attrs)
        if current_crs is not None:
            array_crs[array_name] = current_crs

    unique_crs = set(array_crs.values())
    if unique_crs:
        first_crs = unique_crs.pop()
        if len(unique_crs) > 0:
            logger.warning(
                "Found multiple CRS values in the Zarr dataset, "
                "using the first one: %s",
                first_crs,
            )
        return first_crs

    lat_dim_name = find_latitude_dimension(dset)
    lon_dim_name = find_longitude_dimension(dset)
    if lat_dim_name is not None and lon_dim_name is not None:
        return CRS.from_epsg(4326)

    return None


def _coordinates_are_top_left(dset: xr.Dataset) -> bool:
    """Tries to figure out whether coordinates are top left

    Except for the case where the top-left coordinate is (-180, 90) we can't be sure
    though. So this only captures the simple case
    """
    if dset.rio.crs != WGS84_CRS:
        return False

    lon = dset["x"]
    lat = dset["y"]
    return bool(lat[0] == 90 and lon[0] == -180)


def _shift_coordinates_from_top_left_to_pixel_center(dset: xr.Dataset) -> xr.Dataset:
    """Shifts the coordinates from the top left to the pixel center"""
    lon = dset["x"]
    lat = dset["y"]

    res_x, res_y = dset.rio.resolution()

    lon_center = lon + res_x / 2
    lat_center = lat + res_y / 2
    dset["x"] = lon_center
    dset["y"] = lat_center

    return dset


class ZarrDatasetDefinition(DatasetDefinition):
    store: str
    rename: dict[str, str] | None
    kw_args: dict[str, Any] | None


class ZarrDataset(RasterDataset[ZarrDatasetDefinition]):
    """Dataset based on a Zarr store.

    When loading into xarray, this dataset type will automatically standardize the
    dimensions of the dataset to 'y', 'x' and 'time' if present. It will try to infer
    spatial dimensions, so if 'lon' or 'longitude' is present, it will be renamed to
    'x'.

    This only supports datasets with 2 or 3 dimensions. If an additional dimension like
    'band' is present, it will be renamed to 'band_1', 'band_2' etc. If more than one
    additional dimension is present, a `ValueError` will be raised.

    Args:
        store:
            The Zarr store to load the dataset from. Can contain a single placeholder
            with a dimension name, e.g. `gs://data/{time}.zarr`. If specified, this
            concatenates multiple Zarrs along either an existing or new dimension as
            named in the pattern. In the above example, all Zarrs found for the glob
            `gs://data/*.zarr` are concatenated along the `time` dimension. If the time
            dimension does not already exist, it is created.
        name:
            The name of the dataset. Defaults to a random UUID. If explicitly given, the
            dataset will be visible in the Earthscale platform.
        rename:
            A dictionary mapping the original dimension names to the desired dimension
            names.
        kwargs:
            Additional keyword arguments to pass to `xarray.open_zarr`.

    """

    def __init__(
        self,
        store: str | Path,
        name: str | None = None,
        attributes: dict[str, str] | None = None,
        metadata: DatasetMetadata | None = None,
        rename: dict[str, str] | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
        **kwargs: Any | None,
    ):
        # run parsing now to validate early for the user
        parse_dimension_placeholder_path(store)
        explicit_name = name is not None
        name = name or str(uuid.uuid4())

        self._store = store
        self._rename = rename
        self._kwargs = kwargs

        definition = ZarrDatasetDefinition(
            store=str(store),
            rename=rename,
            kw_args=kwargs,
        )

        # There's no use for bbox or bands here as the performance is the same whether
        # the whole dataset metadata is loaded or not
        def load(
            bbox: BBOX | GeoBox | None,
            bands: Iterable[str] | None,
            chunksizes: Chunksizes | None,
            memory_limit_megabytes: int,
            extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
        ) -> xr.Dataset:
            logger.debug("Calling load function for ZarrDataset")
            return _load_zarr_dataset(
                store=store,
                rename=rename or {},
                bbox=bbox,
                bands=bands,
                memory_limit_megabytes=memory_limit_megabytes,
                extra_dimension_selector=extra_dimension_selector,
                **kwargs,
            )

        graph = create_source_graph(
            f"load_zarr_dataset_{name}",
            name,
            metadata,
            load,
        )

        super().__init__(
            name=name,
            explicit_name=explicit_name,
            attributes=attributes,
            graph=graph,
            metadata=metadata or DatasetMetadata(),
            # We want the geobox of the full dataset as well as all bands here, so not
            # passing a bounding box here
            geobox_callback=lambda: load(
                bbox=None,
                bands=None,
                chunksizes=None,
                memory_limit_megabytes=0,
                extra_dimension_selector={},
            ).odc.geobox,
            definition=definition,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    @property
    def data_region(self) -> str | None:
        if self._data_region is not None:
            return self._data_region

        if isinstance(self._store, str) and is_gcs_url(self._store):
            self._data_region = get_region_from_gcs_url(self._store)

        return self._data_region

    def get_dimension_info(self) -> DimensionInfo:
        return get_dimensions_from_dataset(self)


def _fix_0_to_360_lon(dset: xr.Dataset, degree_tolerance: float = 10) -> xr.Dataset:
    # Consider the dataset 0-360 if min is 0°+-10° and max is 360°+-10°
    if "x" not in dset:
        logger.error("Cannot fix lon values for dataset without x dimension")
        return dset
    x_dim = dset["x"]
    x_range = x_dim.min(), x_dim.max()
    if abs(x_range[0]) > degree_tolerance or abs(360 - x_range[1]) > degree_tolerance:
        return dset
    logger.debug("Fixing lon values for dataset with 0-360 lon range")
    resolution = dset.odc.geobox.resolution.x
    if resolution is None or resolution < 1e-6:
        logger.error("Cannot fix lon values for dataset without x resolution")
        return dset
    roll_distance = int(round(-180 / resolution))
    dset = dset.roll({"x": roll_distance}, roll_coords=False)
    dset["x"] = dset["x"] - 180
    dset = dset.assign_coords(xr_coords(dset.odc.geobox, dims=dset.odc.spatial_dims))
    return dset


def _fix_0_to_180_lat(dset: xr.Dataset, degree_tolerance: float = 10) -> xr.Dataset:
    # Consider the dataset 0-180 if min is 0°+-10° and max is 180°+-10°
    if "y" not in dset:
        logger.error("Cannot fix lat values for dataset without y dimension")
        return dset
    y_dim = dset["y"]
    y_range = y_dim.min(), y_dim.max()
    if abs(y_range[0]) > degree_tolerance or abs(180 - y_range[1]) > degree_tolerance:
        return dset
    logger.debug("Fixing lat values for dataset with 0-180 lat range")
    resolution = dset.odc.geobox.resolution.y
    if resolution is None or resolution < 1e-6:
        logger.error("Cannot fix lat values for dataset without y resolution")
        return dset
    roll_distance = int(round(-90 / resolution))
    dset = dset.roll({"y": roll_distance}, roll_coords=False)
    dset["y"] = dset["y"] - 90
    dset = dset.assign_coords(xr_coords(dset.odc.geobox, dims=dset.odc.spatial_dims))
    return dset


def _open_single_zarr(
    mapper: fsspec.FSMap,
    rename: dict[str, str] | None = None,
    bands: Iterable[str] | None = None,
    **kwargs: Any,
) -> xr.Dataset:
    # .get_mapper inspired by: https://github.com/fsspec/filesystem_spec/issues/386
    # Try to decode coordinates first, then fall back to default.
    kwargs = copy(kwargs) or {}
    kwargs["decode_coords"] = kwargs.get("decode_coords", "all")

    used_coords_fallback = False
    used_time_fallback = False
    while not all([used_time_fallback, used_coords_fallback]):
        try:
            dset = xr.decode_cf(xr.open_zarr(mapper, **kwargs))
            if rename:
                dset = dset.rename(rename)
            if bands:
                dset = dset[list(bands)]  # Convert to list to ensure we get a Dataset
            return dset
        except ValueError as e:
            if used_time_fallback or "decode_times=False" not in str(e.args[0]):
                raise
            logger.debug(
                "Failed to decode time coordinates for dataset. "
                "Trying to fallback to decode_times=False"
            )
            kwargs["decode_times"] = False
            used_time_fallback = True
        except AttributeError as e:
            if used_coords_fallback:
                raise
            logger.debug(
                f"Failed to load Zarr dataset with decode_coords=all: {e}. Falling back"
                f" to default."
            )
            kwargs["decode_coords"] = True
            used_coords_fallback = True
    raise RuntimeError(
        f"Failed to open Zarr datasets from {mapper} after using multiple fallbacks. "
    )


def _get_dset_mean_num_spatial_pixels(
    dset: xr.Dataset,
) -> float:
    """
    Gets the average number of spatial pixels in the dset over all data arrays and
    dimensions.
    """
    num_data_vars = len(dset.data_vars)
    if num_data_vars == 0:
        return 0
    src_spatial_dims = spatial_dims(dset)
    if src_spatial_dims is None:
        return sum(da.size for da in dset.data_vars.values()) / num_data_vars
    return (
        sum(
            float(
                np.prod([da.sizes[dim] for dim in src_spatial_dims if dim in da.dims])
            )
            for da in dset.data_vars.values()
        )
        / num_data_vars
    )


def _check_reproject_memory_limit(
    src_dset: xr.Dataset,
    dst_geobox: GeoBox,
    memory_limit_megabytes: int,
) -> None:
    src_npixels = _get_dset_mean_num_spatial_pixels(src_dset)
    if src_npixels == 0:
        return
    src_nbytes = src_dset.nbytes
    bytes_per_pixel = src_nbytes / src_npixels

    src_geobox: GeoBox = src_dset.odc.geobox
    assert src_geobox.crs is not None

    # we are computing the input to the reprojection, so we need to swap src and dst
    read_geobox = compute_output_geobox_without_buffering(
        src_geobox=dst_geobox,
        dst_crs=src_geobox.crs,
        dst_resolution=src_geobox.resolution,
        dst_anchor=src_geobox.anchor,
    )

    bytes_to_read = bytes_per_pixel * read_geobox.shape[0] * read_geobox.shape[1]
    required_mb = bytes_to_read / 1024 / 1024
    if required_mb > memory_limit_megabytes:
        raise MemoryLimitExceededError(
            required_megabytes=required_mb,
            limit_megabytes=memory_limit_megabytes,
        )


def _crop_and_reproject_zarr_dataset(
    src_dset: xr.Dataset,
    dst_bbox: GeoBox,
    memory_limit_megabytes: int,
) -> xr.Dataset:
    src_geobox: GeoBox = src_dset.odc.geobox
    if dst_bbox.crs == src_geobox.crs:
        try:
            src_dset = xr_reproject(
                src=src_dset,
                how=dst_bbox,
            )
        except IndexError as e:
            # odc geo raises an index error if the windows are non-overlapping
            raise NoDataInSelectionError(
                "Output bbox does not overlap with dataset"
            ) from e
        return src_dset

    dst_crs = dst_bbox.crs
    if dst_crs is None:
        raise ValueError("Destination GeoBox must have a CRS")

    # For reprojecting, we limit the size to avoid memory issues
    # The limit is based on how much data we will need to load to reproject
    if memory_limit_megabytes > 0:
        _check_reproject_memory_limit(src_dset, dst_bbox, memory_limit_megabytes)
    src_dset = src_dset.rio.clip_box(
        *dst_bbox.boundingbox,
        crs=dst_bbox.crs,
        auto_expand=True,
    )
    if dst_bbox.crs is not None and dst_bbox.crs.to_epsg() == 3857:
        dst_bbox = clip_geobox(dst_bbox, _WEB_MERCATOR_BBOX)

    dst_chunk_size = (
        min(dst_bbox.shape[0], 2048),
        min(dst_bbox.shape[1], 2048),
    )
    src_dset = xr_reproject(
        src=src_dset,
        how=dst_bbox,
        resampling="nearest",
        chunks=dst_chunk_size,
    )
    return src_dset


def _apply_dimension_selector(
    dset: xr.Dataset,
    extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]] | None = None,
) -> xr.Dataset:
    if extra_dimension_selector is None:
        return dset
    for dim, selector in extra_dimension_selector.items():
        if dim not in dset.dims:
            continue
        # Handle datetime selectors for time dimension
        is_datetime = isinstance(selector, datetime.datetime) or (
            isinstance(selector, tuple)
            and all(isinstance(x, datetime.datetime) for x in selector)
        )
        if is_datetime:
            if isinstance(selector, tuple):
                start, end = selector
                selector = (
                    np.datetime64(utc_datetime(start)),
                    np.datetime64(utc_datetime(end)),
                )
            else:
                selector = np.datetime64(utc_datetime(selector))

        # Apply selector
        if isinstance(selector, tuple):
            dset = dset.sel({dim: slice(*selector)})
        else:
            dset = dset.sel({dim: selector})

    return dset


def _load_zarr_dataset(
    store: str | Path,
    rename: dict[str, str],
    bbox: BBOX | GeoBox | None,
    bands: Iterable[str] | None,
    memory_limit_megabytes: int,
    extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]] | None = None,
    **kwargs: Any | None,
) -> xr.Dataset:
    kwargs = kwargs or {}

    store, concat_dim_name = parse_dimension_placeholder_path(store)
    storage_options = get_fsspec_storage_options(str(store))
    extra_dimension_selector = extra_dimension_selector or {}

    if concat_dim_name is not None:
        # fsspec glob does not work as documented with paths ending in slashes
        # (supposedly returns only directories, but that seems to be broken in gcs)
        if isinstance(store, str):
            store = store.rstrip("/")
        dsets: list[tuple[str, xr.Dataset]] = []
        errors: list[tuple[str, Exception]] = []
        fs: fsspec.AbstractFileSystem
        fs, _ = fsspec.url_to_fs(store, **storage_options)
        paths = cast(list[str], fs.glob(store, maxdepth=1))
        logger.info(
            "Opening {num} Zarrs from {store}",
            num=len(paths),
            store=store,
        )
        if len(paths) > 10:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for path in paths:
                    futures.append(
                        executor.submit(
                            _try_to_open_globbed_zarr,
                            path=path,
                            fs=fs,
                            store=store,
                            rename=rename,
                            bands=bands,
                            kwargs=kwargs,
                            dsets=dsets,
                            errors=errors,
                        )
                    )
                concurrent.futures.wait(futures, timeout=120)
        else:
            for path in paths:
                _try_to_open_globbed_zarr(
                    path=path,
                    fs=fs,
                    store=store,
                    rename=rename,
                    bands=bands,
                    kwargs=kwargs,
                    dsets=dsets,
                    errors=errors,
                )
        logger.info(
            "Opened {num_ds} Zarrs from {store}",
            num_ds=len(dsets),
            store=store,
        )

        if not dsets:
            if not errors:
                raise NoFilesForGlobError(f"No Zarrs found for glob path {store}")
            errors_str = "\n".join(": ".join(map(str, i)) for i in errors)
            raise NoFilesForGlobError(
                f"Could not open any Zarrs found by glob path {store}. Some failed "
                f"with errors: \n{errors_str}"
            )
        dset = xr.concat((d[1] for d in dsets), dim=concat_dim_name)
        dset = dset.sortby(concat_dim_name)
    else:
        mapper = fsspec.get_mapper(
            glob.escape(str(store)),
            **storage_options,
        )
        dset = _open_single_zarr(mapper, rename=rename, **kwargs)
        dset = _fixup_zarr(dset)

    # Apply dimension selection
    dset = _apply_dimension_selector(dset, extra_dimension_selector)

    if isinstance(bbox, GeoBox):
        dset = _crop_and_reproject_zarr_dataset(dset, bbox, memory_limit_megabytes)
    return dset


def _fixup_zarr(dset: xr.Dataset) -> xr.Dataset:
    crs: CRS | None = CRS(dset.odc.crs) if dset.odc.crs else None
    if crs is None:
        crs = _detect_zarr_crs(dset)

    # Search for common y dimension name among dim names and normalize to y if found
    y_dim_name = find_latitude_dimension(dset) or find_y_dimension(dset)
    if y_dim_name and y_dim_name != "y":
        dset = dset.rename({y_dim_name: "y"})

    # Search among common x dimension name among dim names and normalize to x if found
    x_dim_name = find_longitude_dimension(dset) or find_x_dimension(dset)
    if x_dim_name and x_dim_name != "x":
        dset = dset.rename({x_dim_name: "x"})

    if crs is None:
        logger.warning(
            "No CRS found in Zarr dataset. Guessing based on coordinate ranges."
        )
        crs = _guess_crs_from_coords(dset.x, dset.y)
    dset = dset.odc.assign_crs(crs=crs)

    # detect 0-360 longitude or 0-180 latitude (VIDA)
    if crs.is_geographic:
        dset = _fix_0_to_360_lon(dset)
        dset = _fix_0_to_180_lat(dset)

    if _coordinates_are_top_left(dset):
        dset = _shift_coordinates_from_top_left_to_pixel_center(dset)

    # detect time encoded as small integers (years) and convert to regular time
    if "time" in dset.coords:
        time_coord = dset.coords["time"]
        if np.issubdtype(time_coord.dtype, np.integer):
            max_time: int = time_coord.max().item()
            if max_time < 10_000:
                # These are year numbers, as integers
                time_coord = time_coord.astype(np.uint64)
                time_coord.data[:] = pd.to_datetime(time_coord.data, format="%Y")
                time_coord = time_coord.astype("datetime64[ns]")

                dset.coords["time"] = time_coord
    return dset


def _try_to_open_globbed_zarr(
    path: str | Path,
    fs: fsspec.AbstractFileSystem,
    store: str | Path,
    rename: dict[str, str],
    bands: Iterable[str] | None,
    kwargs: dict[str, Any],
    dsets: list[tuple[str, xr.Dataset]],
    errors: list[tuple[str, Exception]],
) -> None:
    try:
        dsets.append(
            (
                str(path),
                _fixup_zarr(
                    _open_single_zarr(
                        fs.get_mapper(str(path)),
                        rename=rename,
                        bands=bands,
                        **kwargs,
                    )
                ),
            )
        )
    except Exception as e:
        errors.append((str(path), e))
        logger.error(
            "Could not open dataset {path} found by glob path "
            "{store} with error: {e}",
            path=path,
            store=store,
            e=e,
        )


def _guess_crs_from_coords(x: np.ndarray[Any, Any], y: np.ndarray[Any, Any]) -> CRS:
    """Guess the CRS based on x/y coordinate ranges.

    VERY rough guess based on coordinate ranges.

    Args:
        x: Array of x coordinates
        y: Array of y coordinates

    Returns:
        Guessed CRS (defaults to EPSG:4326 if unable to determine)

    Common cases:
        - EPSG:4326 (WGS84): x: [-180, 180], y: [-90, 90]
        - EPSG:3857 (Web Mercator): x/y: [-20037508.34, 20037508.34]
    """
    x_min, x_max = float(x.min()), float(x.max())
    y_min, y_max = float(y.min()), float(y.max())

    # Check for WGS84 range first
    if -180 <= x_min <= x_max <= 180 and -90 <= y_min <= y_max <= 90:
        return CRS.from_epsg(4326)

    # Only guess Web Mercator if coordinates are clearly in that range
    # (significantly larger than WGS84 bounds)
    WEB_MERCATOR_BOUND = 20037508.34
    if (
        abs(x_min) > 180
        and abs(x_max) > 180
        and abs(y_min) > 90
        and abs(y_max) > 90
        and abs(x_min) <= WEB_MERCATOR_BOUND
        and abs(x_max) <= WEB_MERCATOR_BOUND
        and abs(y_min) <= WEB_MERCATOR_BOUND
        and abs(y_max) <= WEB_MERCATOR_BOUND
    ):
        return CRS.from_epsg(3857)

    # Default to WGS84 if unable to determine
    logger.warning(
        f"Unable to definitively determine CRS from coordinate ranges: "
        f"x: [{x_min}, {x_max}], y: [{y_min}, {y_max}]. Defaulting to EPSG:4326"
    )
    return CRS.from_epsg(4326)
