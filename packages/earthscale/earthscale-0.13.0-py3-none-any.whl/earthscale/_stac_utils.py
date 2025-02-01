import datetime
import fnmatch
import functools
import re
import time
import uuid
from collections import defaultdict
from collections.abc import Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from typing import Any, cast

import numpy as np
import odc.stac
import pandas as pd
import rasterio
import xarray as xr
from loguru import logger
from odc.geo import BoundingBox
from odc.geo.geobox import GeoBox
from odc.stac import output_geobox, parse_items
from pydantic import BaseModel
from pyproj import CRS
from pystac import Item
from rasterio import DatasetReader, RasterioIOError
from rio_stac import create_stac_item
from rio_stac.stac import RASTER_EXT_VERSION

from earthscale.auth import get_gdal_options_for_url
from earthscale.constants import DEFAULT_CHUNKSIZES, MAX_NUM_EO_ASSET_BANDS
from earthscale.exceptions import NoSTACItemsError, convert_rasterio_to_earthscale
from earthscale.odc_geo_extensions import bbox_intersects
from earthscale.raster_utils import (
    detect_crs_from_cf_convention_tags,
    detect_datetime_from_cf_convention_tags,
)
from earthscale.types import BBOX, Chunksizes, Groupby
from earthscale.utils import utc_datetime

_DEFAULT_DATETIME = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
# Arguments other than `geobox` that `odc.stac.load` uses for georeferencing
_GEOREFERENCING_ARGS = (
    "x",
    "y",
    "lon",
    "lat",
    "crs",
    "resolution",
    "align",
    "anchor",
    "like",
    "geopolygon",
    "bbox",
)


class FilenameBandPattern(BaseModel):
    pattern: str
    band: str


# Using a lower `maxsize` as the images are potentially quite large
@functools.lru_cache(maxsize=10)
def convert_stac_items_to_geobox(
    items: tuple[Item, ...],
    bands: tuple[str, ...] | None,
    **kwargs: Any,
) -> GeoBox:
    logger.debug("Converting STAC items to geobox")
    geobox = output_geobox(
        items=list(parse_items(items)),
        bands=bands,
        crs=kwargs.get("crs"),
        resolution=kwargs.get("resolution"),
        anchor=kwargs.get("anchor"),
        align=kwargs.get("align"),
        geobox=kwargs.get("geobox"),
        like=kwargs.get("like"),
        geopolygon=kwargs.get("geopolygon"),
        bbox=kwargs.get("bbox"),
        lon=kwargs.get("lon"),
        lat=kwargs.get("lat"),
        x=kwargs.get("x"),
        y=kwargs.get("y"),
    )
    if geobox is None:
        raise ValueError(
            "Could not determine geobox for dataset. "
            "Ensure that the items have the proj STAC extension or pass "
            "in a geobox or crs, resulution, and bbox explicitly."
        )
    return geobox


def _parse_datetime_from_string(
    date_string: str, date_format: str
) -> datetime.datetime:
    # Convert strptime format codes to regex patterns
    format_to_pattern = {
        "%Y": r"\d{4}",
        "%y": r"\d{2}",
        "%m": r"\d{2}",
        "%d": r"\d{2}",
        "%H": r"\d{2}",
        "%M": r"\d{2}",
        "%S": r"\d{2}",
    }

    # Build regex pattern from date format
    pattern = date_format
    for format_code, regex in format_to_pattern.items():
        pattern = pattern.replace(format_code, f"({regex})")

    # Find matching substring using regex

    match = re.search(pattern, date_string)
    if not match:
        raise ValueError(
            f"Could not find date matching format {date_format} in {date_string}"
        )

    # Extract the matching substring
    date_substring = match.group(0)

    # Parse the date
    date = datetime.datetime.strptime(date_substring, date_format)
    return date


# Copied from rio-stac
# https://github.com/developmentseed/rio-stac/blob/52a13eec0c8ad19dee904b2bc0cd529b73b95899/rio_stac/stac.py#
# but removed stats creation for performance reasons as it takes too long for rasters
# with a lot of bands and we don't use it yet
def _get_raster_info(src_dst: DatasetReader) -> list[dict[str, Any]]:
    """Get raster metadata.

    see: https://github.com/stac-extensions/raster#raster-band-object

    """
    meta: list[dict[str, Any]] = []

    area_or_point = src_dst.tags().get("AREA_OR_POINT", "").lower()

    # Missing `bits_per_sample` and `spatial_resolution`
    for band in src_dst.indexes:
        value = {
            "data_type": src_dst.dtypes[band - 1],
            "scale": src_dst.scales[band - 1],
            "offset": src_dst.offsets[band - 1],
        }
        if area_or_point:
            value["sampling"] = area_or_point

        # If the Nodata is not set we don't forward it.
        if src_dst.nodata is not None:
            if np.isnan(src_dst.nodata):
                value["nodata"] = "nan"
            elif np.isposinf(src_dst.nodata):
                value["nodata"] = "inf"
            elif np.isneginf(src_dst.nodata):
                value["nodata"] = "-inf"
            else:
                value["nodata"] = src_dst.nodata

        if src_dst.units[band - 1] is not None:
            value["unit"] = src_dst.units[band - 1]

        meta.append(value)

    return meta


def _create_stac_item_from_one_url(
    ds: DatasetReader,
    datetime_: datetime.datetime | None,
    properties: dict[str, Any] | None,
) -> Item:
    raster_bands = _get_raster_info(ds)

    item: Item = create_stac_item(
        ds,
        input_datetime=datetime_,
        with_proj=True,
        # We are not adding the `eo` extension as that adds a significant overhead to
        # `odc.stac.load`
        with_eo=False,
        properties=properties,
    )
    item.stac_extensions.append(
        f"https://stac-extensions.github.io/raster/{RASTER_EXT_VERSION}/schema.json",
    )
    assert len(item.assets) == 1
    first_asset = next(iter(item.assets.values()))
    first_asset.extra_fields["raster:bands"] = raster_bands
    first_asset.media_type = "image/tiff"
    props = item.properties
    if (
        props.get("proj:epsg") is None
        and props.get("proj:wkt2") is None
        and props.get("projjson") is None
    ):
        detected_crs = detect_crs_from_cf_convention_tags(ds.tags())
        if detected_crs is None:
            raise ValueError(
                "Could not detect the CRS of the dataset. Please make sure that "
                "gdalinfo outputs a valid CRS for this dataset or contact us if you "
                "think we should be able to detect it automatically."
            )
        props["proj:wkt2"] = detected_crs.to_wkt()
    if item.datetime is None or item.datetime == datetime.datetime(
        1970, 1, 1, tzinfo=datetime.timezone.utc
    ):
        detected_datetime = detect_datetime_from_cf_convention_tags(ds.tags())
        if detected_datetime is not None:
            item.datetime = detected_datetime
    return item


def _get_datetime_and_properties_for_url(
    url: str,
    datetime_: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None,
    filename_date_pattern: str | None,
    band_info: pd.DataFrame | None,
) -> tuple[datetime.datetime | None, dict[str, Any]]:
    """
    Get the datetime and start/end datetime Item properties for a given URL.
    """
    final_datetime = None
    datetime_props = {}

    if isinstance(datetime_, datetime.datetime):
        final_datetime = datetime_
    elif isinstance(datetime_, tuple):
        datetime_props["start_datetime"] = datetime_[0].isoformat()
        datetime_props["end_datetime"] = datetime_[1].isoformat()
        final_datetime = None
    elif filename_date_pattern is not None:
        try:
            final_datetime = _parse_datetime_from_string(url, filename_date_pattern)
        except ValueError as e:
            logger.error(f"Failed to parse datetime from asset {url}: {e}")
            raise e
    elif band_info is not None and "datetime" in band_info.columns:
        min_datetime = band_info["datetime"].min()
        max_datetime = band_info["datetime"].max()
        datetime_props["start_datetime"] = min_datetime.isoformat()
        datetime_props["end_datetime"] = max_datetime.isoformat()
        final_datetime = None
    else:
        final_datetime = _DEFAULT_DATETIME

    return final_datetime, datetime_props


def create_stac_items_from_urls(
    urls: list[str],
    datetime_: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None,
    filename_date_pattern: str | None,
    band_info: pd.DataFrame | None,
    filename_band_pattern: list[FilenameBandPattern] | None,
) -> list[Item]:
    # In the case no time information is provided, we default to the Unix epoch.
    # The time information will be set by the bands on the outside.
    if datetime_ is None and filename_date_pattern is None:
        datetime_ = _DEFAULT_DATETIME

    properties = {}
    if isinstance(datetime_, tuple):
        properties["start_datetime"] = datetime_[0].isoformat()
        properties["end_datetime"] = datetime_[1].isoformat()
        datetime_ = None

    def process_url(
        url: str,
    ) -> Item:
        url_properties = deepcopy(properties)
        url_datetime, datetime_props = _get_datetime_and_properties_for_url(
            url, datetime_, filename_date_pattern, band_info
        )
        url_properties.update(datetime_props)

        gdal_options = get_gdal_options_for_url(url)
        try:
            with rasterio.Env(**gdal_options), rasterio.open(url, "r") as ds:
                item = _create_stac_item_from_one_url(ds, url_datetime, properties)
                if filename_band_pattern is not None:
                    # We sort the patterns by length to ensure we match the most
                    # specific pattern first.
                    sorted_patterns = sorted(
                        filename_band_pattern,
                        key=lambda pattern_and_band: len(pattern_and_band.pattern),
                        reverse=True,
                    )
                    for band_pattern in sorted_patterns:
                        pattern = band_pattern.pattern.lower()
                        band = band_pattern.band
                        if fnmatch.fnmatch(url.lower(), pattern):
                            # Get the first (and only) asset
                            asset = next(iter(item.assets.values()))

                            # Create new assets dict with band name as key
                            new_assets = {band: asset}

                            # Replace the assets dict
                            item.assets = new_assets
                            break
                return item
        except RasterioIOError as e:
            if "GS_SECRET_ACCESS_KEY" in e.args[0]:
                logger.error(
                    f"Error opening {url}. Do you have the correct credentials"
                    " to access this dataset?"
                )
            raise e

    logger.info(f"Processing {len(urls)} URLs")

    with ThreadPoolExecutor(max_workers=128) as executor:
        items = list(executor.map(lambda url: process_url(url), urls))
    return items


def _get_stac_item_boundingbox(item: Item) -> BoundingBox:
    if item.bbox is None:
        return BoundingBox(
            left=-180,
            bottom=-90,
            right=180,
            top=90,
            crs=CRS.from_epsg(4326),
        )
    return BoundingBox(
        left=item.bbox[0],
        bottom=item.bbox[1],
        right=item.bbox[2],
        top=item.bbox[3],
        crs=CRS.from_epsg(4326),
    )


def _reshape_dset_to_band_info(
    dset: xr.Dataset,
    bands: Iterable[str] | None,
    band_info: pd.DataFrame,
) -> xr.Dataset:
    """
    ODC STAC output dataset originally has one data variable per datetime+band.
    This function reshapes it to have one data variable per band, with
    datetimes as coordinates.
    """
    dataarrays_per_band = defaultdict(list)

    relevant_band_info = band_info
    if bands is not None:
        relevant_band_info = band_info[band_info["name"].isin(bands)]

    if "datetime" in relevant_band_info.columns:
        for row_index, row in relevant_band_info.iterrows():
            if not isinstance(row_index, int):
                raise ValueError(
                    "The index of the band info dataframe must be an integer"
                )
            # Band names will be `asset.<i>` (1-indexed)
            current_band_name = f"asset.{row_index + 1}"
            new_band_name = row["name"]
            dataarray = (
                dset[current_band_name]
                .squeeze()
                .expand_dims({"time": [row["datetime"]]})
            )
            dataarrays_per_band[new_band_name].append(dataarray)
        # Concatenate all DataArrays along the time dimension
        concatenated_dataarrays = {
            band_name: xr.concat(dataarrays, dim="time")
            for band_name, dataarrays in dataarrays_per_band.items()
        }
        # convert back to Dataset
        new_dset = xr.Dataset(concatenated_dataarrays)
    else:
        rename_dict = {
            f"asset.{cast(int, i) + 1}": row["name"]
            for i, row in relevant_band_info.iterrows()
        }
        new_dset = dset.rename_vars(rename_dict)

    return new_dset


def load_stac_dataset(  # noqa: C901
    items: list[Item],
    bands: Iterable[str] | None,
    groupby: Groupby | None,
    # Geobox of the full dataset, enabling a subselection of bbox in the same pixel grid
    full_geobox: GeoBox | None = None,
    # BBOX is assumed to be in EPSG:4326
    bbox: BBOX | GeoBox | None = None,
    chunksizes: Chunksizes | None = None,
    band_info: pd.DataFrame | None = None,
    extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]] | None = None,
    **kwargs: Any | None,
) -> xr.Dataset:
    extra_dimension_selector = extra_dimension_selector or {}
    if chunksizes is None:
        chunksizes = DEFAULT_CHUNKSIZES

    original_number_of_items = len(items)

    # Filter by datetime if provided
    time_selector = extra_dimension_selector.get("time")
    # FIXME: Add other cases
    if isinstance(time_selector, datetime.datetime):
        datetime_ = time_selector
        # As per the STAC spec, all datetimes in the stac item are in UTC
        # https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#datetime
        utc_datetime_ = utc_datetime(datetime_)
        # Convert to UTC, since we saw both with and without tzinfo
        for item in items:
            if item.datetime is not None and item.datetime.tzinfo is not None:
                item.datetime = utc_datetime(item.datetime)
        items = [item for item in items if item.datetime == utc_datetime_]
        logger.debug(
            f"Filtering by datetime {datetime_} reduced the number of items from "
            f"{original_number_of_items} to {len(items)}"
        )

    geobox_to_load = None
    if bbox is not None:
        if full_geobox is None:
            raise ValueError(
                "Cannot provide a bounding box without a full geobox of the dataset"
            )

        # Not 100% sure whether this filtering is strictly necessary, but the time to
        # filter the elements is negligible

        # STAC item bbox is in EPSG:4326, see
        # https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#bbox
        if isinstance(bbox, GeoBox):
            query_boundingbox = bbox.boundingbox.to_crs(CRS.from_epsg(4326))
        else:
            query_boundingbox = BoundingBox(*bbox, crs=CRS.from_epsg(4326))
        items = [
            item
            for item in items
            if bbox_intersects(
                _get_stac_item_boundingbox(item),
                query_boundingbox,
            )
        ]

        if isinstance(bbox, GeoBox):
            # If we specied a resolution and alignment, we want to keep it!
            # This helps to read from the correct overview level, and also ensures the
            # correct pixel alignment in the output
            geobox_to_load = bbox
        else:
            # Else, this ensures that the pixel alignment of the input is kept
            geobox_to_load = full_geobox.enclosing(query_boundingbox)
        # When geobox is provided kwargs must not include any other georeferencing
        # arguments
        for arg in _GEOREFERENCING_ARGS:
            if arg in kwargs:
                del kwargs[arg]

    if len(items) == 0:
        logger.info(
            "No items remain after spatial and temporal filtering, raising a "
            "NoSTACItemsError"
        )
        raise NoSTACItemsError
    else:
        logger.debug(
            f"Spatial and temporal filtering reduced the number of items from "
            f"{original_number_of_items} to {len(items)}"
        )

    if kwargs is None:
        kwargs = {}

    selected_bands: list[str] | None = None

    # We've had some trouble with datetime serialization, so we're making sure the
    # datetime column is always of the correct type
    if band_info is not None and "datetime" in band_info.columns:
        band_info["datetime"] = pd.to_datetime(band_info["datetime"])

    # The bands will be named `asset.<band_index>` (with 1-indexed band index)
    if band_info is not None and bands is not None:
        rows_for_name = band_info[band_info["name"].isin(bands)]
        selected_bands = [f"asset.{index + 1}" for index in rows_for_name.index]
    elif bands is not None:
        selected_bands = list(bands)

    # We only support TIFF files for now. Some STAC catalogs of interest have
    # non-raster assets such as J2 files so we exclude those.
    filtered_items = []
    for item in items:
        filtered_assets = {
            key: asset
            for key, asset in item.assets.items()
            if asset.media_type and "image/tiff" in asset.media_type.lower()
        }
        if filtered_assets:
            filtered_item = item.clone()
            filtered_item.assets = filtered_assets
            filtered_items.append(filtered_item)

    items = filtered_items
    logger.debug(f"Filtered to {len(items)} items with 'image/tiff' assets")

    # Clearing the `eo:bands.name` property if there are too many bands.
    # We're clearing that to have deterministic band names (`asset.<i>`) in the output
    # dset.
    # Generally, this is not great as we're loosing information present in the STAC
    # items, so we'll need to find a better solution there in the future.
    # Having the eo:bands.name property present does incur a significant performance hit
    # if the dataset has many bands though
    use_asset_based_naming = False
    for item in items:
        new_assets = {}
        for asset_key, asset in item.assets.items():
            if "eo:bands" in asset.extra_fields:
                num_bands = len(asset.extra_fields["eo:bands"])
                use_asset_based_naming = num_bands > MAX_NUM_EO_ASSET_BANDS
                if not use_asset_based_naming:
                    # Use band name as key if available
                    for band in asset.extra_fields["eo:bands"]:
                        if "name" in band:
                            new_assets[band["name"]] = asset
                            break
                    else:
                        # If no band name found, keep original asset key
                        new_assets[asset_key] = asset
                else:
                    new_assets[asset_key] = asset
            else:
                new_assets[asset_key] = asset
        item.assets = new_assets
    if use_asset_based_naming and band_info is not None:
        logger.warning(
            "Using asset-based naming for dataset because it either lacks eo:bands "
            f"metadata or has more than {MAX_NUM_EO_ASSET_BANDS} bands. "
            "Assets will be named `asset.<i>` (1-indexed) instead of `band_name`. "
            "To specify band names, use the `band_info` argument."
        )

    start_time = time.time()

    # Using the first item here to determine the GDAL options, assumes the whole
    # collection is homogeneous
    first_url = next(iter(items[0].assets.values())).href
    gdal_options = get_gdal_options_for_url(first_url)
    odc.stac.configure_rio(**gdal_options)  # type: ignore

    logger.debug(f"odc.stac.load called with {len(items)} items")

    # To make sure all images are put onto the same plane we're using a random string
    # which is guaranteed to not exist in the item's property. The lookup of the string
    # will return None, resulting in all image to be put onto the same plane.
    if groupby == "one_plane":
        groupby = str(uuid.uuid4())
    try:
        dset = odc.stac.load(
            items=items,
            bands=selected_bands,
            groupby=groupby,
            # This will overwrite any other georeferencing settings such as CRS, x/y,
            # etc. Given that we're only doing this for a bounding box of the "original"
            # dataset this should be ok.
            geobox=geobox_to_load,
            chunks=chunksizes,  # type: ignore
            **kwargs,  # type: ignore
        )
    except RasterioIOError as e:
        raise convert_rasterio_to_earthscale(e) from e
    logger.debug(f"odc.stac.load took {time.time() - start_time} seconds")

    # In the case there's only one band, the band name is sometimes "asset" instead of
    # "asset.1". Fixing that here to make sure downstream code works as expected
    if len(dset.data_vars) == 1 and "asset" in dset.data_vars:
        dset = dset.rename_vars({"asset": "asset.1"})

    # At the moment, the downstream code is assuming no band names are present (e.g.
    # through the `eo:bands.name` STAC extension, just making sure that's the case.
    # Without the band names, we're expecting the data vars to be called `asset.<i>`
    # where `i` is the 1-indexed band index.
    if use_asset_based_naming:
        expected_band_name = re.compile(r"asset\.\d")
        for data_var in dset.data_vars:
            data_var = cast(str, data_var)
            if not expected_band_name.match(data_var):
                raise ValueError(
                    f"Found a data variable {data_var} that does not match the"
                    f"expected pattern 'asset.<i>'"
                )

    # If CRS is WGS84, odc will rename to lat/lng but we require x/y
    rename = {}
    if "longitude" in dset.sizes or "longitude" in dset.coords:
        rename["longitude"] = "x"
    if "latitude" in dset.sizes or "latitude" in dset.coords:
        rename["latitude"] = "y"
    dset = dset.rename(rename)

    if band_info is not None:
        dset = _reshape_dset_to_band_info(dset, bands, band_info)

    if groupby is not None and "time" in dset.sizes:
        # Making sure time is always a date and not a datetime as we only support
        # dates for now
        times = dset["time"].compute()
        dates = times.dt.date.values
        dset["time"] = [
            datetime.datetime(date.year, date.month, date.day) for date in dates
        ]

    # Transpose back to rioxarray conventions
    if "time" in dset.sizes:
        dset = dset.transpose("time", "y", "x", ...)
    else:
        dset = dset.transpose("y", "x", ...)

    # If all dates are equal to _DEFAULT_TIMESTAMP, we assume no time information
    # has been passed in
    if "time" in dset.sizes:
        dset_times = dset["time"].values
        if len(dset_times) == 1 and dset_times[0] == np.datetime64(_DEFAULT_DATETIME):
            dset = dset.isel(time=0)

    return dset
