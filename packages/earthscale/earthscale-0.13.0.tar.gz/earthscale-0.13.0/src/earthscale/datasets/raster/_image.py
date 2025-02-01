import datetime
import uuid
from collections import defaultdict
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import Any, ClassVar

import fsspec
import numpy as np
import pandas as pd
from loguru import logger
from odc.geo.geom import BoundingBox, bbox_union
from pydantic import BaseModel
from pystac import Item
from shapely import GeometryCollection, MultiPolygon, Polygon, box, union_all

from earthscale._stac_utils import (
    FilenameBandPattern,
    convert_stac_items_to_geobox,
    create_stac_items_from_urls,
    load_stac_dataset,
)
from earthscale.auth import get_fsspec_storage_options
from earthscale.datasets.dataset import (
    DatasetDefinition,
    DatasetMetadata,
    DimensionInfo,
)
from earthscale.datasets.graph import (
    create_source_graph,
)
from earthscale.datasets.raster import (
    RasterDataset,
)
from earthscale.datasets.raster._base import get_dimensions_from_dataset
from earthscale.exceptions import NoFilesForGlobError
from earthscale.google_cloud_utils import get_region_from_gcs_url
from earthscale.types import Groupby
from earthscale.utils import create_valid_url, is_gcs_url, is_google_drive_url


def _validate_band_info_dataframe(df: pd.DataFrame) -> None:
    """
    Validate the band info dataframe
    """
    required_columns = {"name"}
    optional_columns = {"min", "max", "datetime"}
    if not required_columns.issubset(df.columns.tolist()):
        raise ValueError(
            f"Band info dataframe must have the following columns: {required_columns}"
        )
    has_extra_columns = set(df.columns.tolist()) - required_columns - optional_columns
    if has_extra_columns:
        raise ValueError(
            f"Band info dataframe has the following extra columns: {has_extra_columns}"
        )

    if "datetime" in df.columns:
        # Check that across each band name, the set of datetimes is the same
        unique_datetimes_per_band = df.groupby("name")["datetime"].unique()
        unique_datetimes = unique_datetimes_per_band.iloc[0]
        for band, datetimes in unique_datetimes_per_band.items():
            if not np.array_equal(unique_datetimes, datetimes):
                raise ValueError(
                    f"Band {band} has different datetimes than the first band. "
                    f"All bands must have the same set of datetimes."
                )


def _update_min_max_metadata(
    metadata: DatasetMetadata,
    band_info: pd.DataFrame,
) -> None:
    """Updates min/max values if both are present in the band info"""
    bands = list(band_info["name"].unique())
    metadata.bands = bands

    rows_with_min_max = band_info[band_info["min"].notna() & band_info["max"].notna()]
    bands_with_min_max = list(rows_with_min_max["name"].unique())

    # Add validation if they only provide min or max, but not both for one band.
    rows_with_only_min = band_info[band_info["min"].notna() & band_info["max"].isna()]
    rows_with_only_max = band_info[band_info["min"].isna() & band_info["max"].notna()]
    if len(rows_with_only_min) > 0 or len(rows_with_only_max) > 0:
        raise ValueError(
            "If specifying min and max values for a band, both must always be provided."
        )

    min_max_values: dict[str, tuple[float | None, float | None]] = {}
    for band in bands_with_min_max:
        orig_band_min = band_info[band_info["name"] == band]["min"].min()
        orig_band_max = band_info[band_info["name"] == band]["max"].max()
        try:
            band_min = float(orig_band_min)
            band_max = float(orig_band_max)
        except Exception as e:
            raise ValueError(
                f"Could not convert min or max values ({orig_band_min}, {orig_band_max}"
                f") for band {band} to float: {e}"
            ) from e
        min_max_values[band] = (band_min, band_max)
    metadata.min_maxes_per_band = min_max_values


class BandInfoRow(BaseModel):
    index: int
    """
    0-based band index
    """
    name: str
    datetime: str | None = None
    min: float | None = None
    max: float | None = None

    # TODO: add validation for datetime


def _band_info_df_to_list(df: pd.DataFrame) -> list[BandInfoRow]:
    # convert any datetimes to isoformat
    if "datetime" in df.columns:
        df["datetime"] = df["datetime"].apply(lambda x: x.isoformat())
    return [
        BandInfoRow(index=idx, **row.to_dict())
        for idx, (_, row) in enumerate(df.iterrows())
    ]


def _band_info_list_to_df(
    band_info: Sequence[BandInfoRow | dict[str, Any]],
) -> pd.DataFrame:
    def _row_to_dict(row: BandInfoRow | dict[str, Any]) -> dict[str, Any]:
        if isinstance(row, BandInfoRow):
            return row.model_dump()
        return row

    df = pd.DataFrame([_row_to_dict(row) for row in band_info])
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])

    # Drop datetime, min or max column if all values are NaN
    df = df.dropna(axis=1, how="all")
    if "index" in df.columns:
        df = df.set_index("index")
    return df


class ImageDatasetDefinition(DatasetDefinition):
    glob_url: str | list[str]
    bands: list[str] | None
    band_info: list[BandInfoRow] | None
    groupby: Groupby | None
    datetime_: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None
    filename_date_pattern: str | None
    filename_band_pattern: list[FilenameBandPattern] | None
    kw_args: dict[str, Any]


GetStacItemsCallback = Callable[[uuid.UUID, str | None], list[Item] | None]


class ImageDataset(RasterDataset[ImageDatasetDefinition]):
    """Dataset based on single images.

     Images must be in a format that can be read by `rasterio`. Under the hood, an
     `ImageDataset` creates a list of STAC items and then uses `odc.stac.load` to load
     the dataset.

     An important concept here is how the time dimension of the `Dataset` is set and
     which images account for which time.

     To group images by time (and thus create a time dimension), you can use the
     `groupby` argument. For more information on the options, please refer to the
     documentation of `odc.stac.load`
     ([here](https://odc-stac.readthedocs.io/en/latest/_api/odc.stac.load.html)). Note
     that as we need to serialize the class, we do not allow callables to be passed in.

     As images generally don't have time information, we provide several ways to set the
     time interval for an image. Only one of the following options can be set:

     1. `band_info`: A pandas DataFrame with band information. This is used to parse
        TIFF band indices into band name and datetime information.
     2. `datetime_`: Either a single `datetime.datetime` or a tuple of two
        `datetime.datetime` objects. If a single `datetime.datetime` is provided, all
        images will have the same timestamp. If a tuple is provided, the first element
        will be the start time and the second element will be the end time. This
        interval will be used for all images. This will result in all images having the
        same time interval.

    Args:
       glob_url:
           URL pattern to find images with. E.g. `gs://bucket/path/to/images/*.tif`.
           Can either be a single string or a list of strings. If a list is given, the
           ordering of the URLs is kept. E.g. images from the first URL will overwrite
           later ones.
       bands:
           List of bands to load. Defaults to all bands.
       band_info:
           DataFrame with band information. Defaults to None. This is used to provide
           metadata about bands in the images. It maps the band index to the band name
           and optionally time, min and max values. The index of the dataframe should be
           the band index (0-indexed). The following columns can be present:
             - name (str; required): The name of the band
             - datetime (datetime.datetime; optional): The datetime of the band
             - min (float; optional): The minimum value of the band
             - max (float; optional): The maximum value of the band
           We also allow this to be passed in as a dictionary of
           {column -> {index -> value}}.
           Can only be used if `datetime_` is not set.
       filename_date_pattern:
            A string pattern representing how dates are formatted in the filenames.
            This pattern uses strftime-style format codes to extract date information.

            Common format codes:
            %Y - Year with century as a decimal number (e.g., 2023)
            %m - Month as a zero-padded decimal number (01-12)
            %d - Day of the month as a zero-padded decimal number (01-31)

            Example:
            - For files named like "brasil_coverage_2011.tif":
              filename_date_pattern="%Y"

            If None (default), no date information will be extracted from filenames.
       filename_band_pattern:
            A dictionary mapping wildcard band name patterns to actual band names.
            E.g. {"*_B[0-9]": "band_1"} would map all bands starting with "B" and
            ending with a number to "band_1". Uses Unix filename pattern rules.
       groupby:
            Controls what items get placed in to the same pixel plane.

            The following have special meaning:

               * "one_plane": All images are loaded into a single plane
               * "time" items with exactly the same timestamp are grouped together
               * "solar_day" items captured on the same day adjusted for solar time
               * "id" every item is loaded separately
               * `None`: No grouping is done, each image is loaded onto an extra plane

            Any other string is assumed to be a key in Item's properties dictionary.
            Please note that contrary to `odc.stac.load` we do not support callables as
            we need to be able to serialize the dataset. Defaults to "one_plane".

       datetime_:
           Either a single `datetime.datetime` or a tuple of two `datetime.datetime`
           objects. If a single `datetime.datetime` is provided, all images will have
           the same time. If a tuple is provided, the first element will be the start
           time and the second element will be the end time. This interval will be
           valid for all images.
           Can only be set if `band_info` is not set.
       name:
           Name of the dataset. Defaults to a random UUID. If explicitly given, the
           dataset will visible in the Earthscale platform
       metadata:
           Dataset Metadata. Defaults to None.
       kwargs:
           Additional keyword arguments to pass to `odc.stac.load`
           (more information in
           [their docs](https://odc-stac.readthedocs.io/en/latest/_api/odc.stac.load.html))

    """

    _GET_ITEMS_CALLBACK: ClassVar[GetStacItemsCallback | None] = None

    @classmethod
    def register_get_items_callback(cls, callback: GetStacItemsCallback) -> None:
        cls._GET_ITEMS_CALLBACK = callback

    def __init__(
        self,
        glob_url: str | list[str],
        bands: list[str] | None = None,
        band_info: pd.DataFrame | Sequence[BandInfoRow | dict[str, Any]] | None = None,
        filename_date_pattern: str | None = None,
        filename_band_pattern: dict[str, str] | list[FilenameBandPattern] | None = None,
        groupby: Groupby | None = "one_plane",
        datetime_: datetime.datetime
        | tuple[datetime.datetime, datetime.datetime]
        | None = None,
        name: str | None = None,
        attributes: dict[str, str] | None = None,
        metadata: DatasetMetadata | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
        **kwargs: Any | None,
    ):
        metadata = metadata or DatasetMetadata()
        explicit_name = name is not None
        name = name or str(uuid.uuid4())
        glob_urls = [glob_url] if isinstance(glob_url, str) else glob_url
        glob_urls = [create_valid_url(url) for url in glob_urls]

        if band_info is not None and datetime_ is not None:
            raise ValueError(
                "Only one of band_info or datetime_ can be used. Both are set."
            )

        if band_info is not None:
            if not isinstance(band_info, pd.DataFrame):
                band_info = _band_info_list_to_df(band_info)
            _validate_band_info_dataframe(band_info)
            has_min = "min" in band_info.columns
            has_max = "max" in band_info.columns
            has_only_one_of_min_max = has_min != has_max
            if has_only_one_of_min_max:
                raise ValueError(
                    "If specifying min and max values for a band, both must be provided"
                )
            if has_min and has_max:
                _update_min_max_metadata(metadata, band_info)

        if isinstance(filename_band_pattern, dict):
            filename_band_pattern = [
                FilenameBandPattern(pattern=pattern, band=band)
                for pattern, band in filename_band_pattern.items()
            ]

        definition = ImageDatasetDefinition(
            glob_url=glob_urls,
            bands=bands,
            band_info=_band_info_df_to_list(band_info)
            if band_info is not None
            else None,
            groupby=groupby,
            datetime_=datetime_,
            filename_date_pattern=filename_date_pattern,
            filename_band_pattern=filename_band_pattern,
            kw_args=kwargs,
        )

        super().__init__(
            name=name,
            explicit_name=explicit_name,
            attributes=attributes,
            graph=create_source_graph(
                f"load_file_dataset_{name}",
                name,
                metadata,
                lambda bbox,
                bands_selection,
                chunksizes,
                memory_limit_megabytes,
                extra_dimension_selector: load_stac_dataset(
                    items=self._items,
                    bands=bands_selection,
                    groupby=groupby,
                    full_geobox=self.geobox,
                    bbox=bbox,
                    chunksizes=chunksizes,
                    band_info=band_info,
                    memory_limit_megabytes=memory_limit_megabytes,
                    extra_dimension_selector=extra_dimension_selector,
                    **kwargs,
                ),
            ),
            metadata=metadata,
            definition=definition,
            geobox_callback=lambda: convert_stac_items_to_geobox(
                tuple(self._items),
                tuple(self.definition.bands) if self.definition.bands else None,
                **self.definition.kw_args,
            ),
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    @cached_property
    def _items(self) -> list[Item]:
        return self.get_items()

    @property
    def data_region(self) -> str | None:
        if self._data_region is not None:
            return self._data_region

        regions_count: dict[str, int] = defaultdict(int)
        for glob_url in self.definition.glob_url:
            if is_gcs_url(glob_url):
                region = get_region_from_gcs_url(glob_url)
                if region is not None:
                    regions_count[region] += 1
        if not regions_count:
            self._data_region = None
            return None
        if len(regions_count) == 1:
            self._data_region = next(iter(regions_count.keys()))
            return self._data_region
        # return the region with the most items
        self._data_region = max(regions_count.items(), key=lambda x: x[1])[0]
        return self._data_region

    def get_items(self) -> list[Item]:
        if ImageDataset._GET_ITEMS_CALLBACK is not None and self._cache_key is not None:
            items = ImageDataset._GET_ITEMS_CALLBACK(self._cache_key, self.data_region)
            if items:
                return items

        logger.debug("Computing items for ImageDataset")
        if self.definition.band_info is not None:
            band_info = _band_info_list_to_df(self.definition.band_info)
        else:
            band_info = None

        # There is no (tested) implementation of fsspec for Google Drive. There is
        # https://github.com/fsspec/gdrivefs but it isn't tested and has no support for
        # shared drives (which we definitely need).
        # As Google Drive does not have globs anyway, we can just return the original
        # URL
        image_urls = []
        glob_urls = (
            [self.definition.glob_url]
            if isinstance(self.definition.glob_url, str)
            else self.definition.glob_url
        )
        for glob_url in glob_urls:
            if is_google_drive_url(glob_url):
                image_urls.append(glob_url)
            else:
                fs, _ = fsspec.url_to_fs(
                    glob_url,
                    **get_fsspec_storage_options(glob_url),
                )
                image_urls.extend(
                    fs.unstrip_protocol(path) for path in fs.glob(glob_url)
                )

        if len(image_urls) == 0:
            raise NoFilesForGlobError(f"No files found for glob urls: {glob_urls}")

        items = create_stac_items_from_urls(
            urls=image_urls,
            datetime_=self.definition.datetime_,
            band_info=band_info,
            filename_date_pattern=self.definition.filename_date_pattern,
            filename_band_pattern=self.definition.filename_band_pattern,
        )
        return items

    def get_dimension_info(self) -> DimensionInfo:
        return get_dimensions_from_dataset(self)

    def get_bounds(self) -> tuple[float, float, float, float]:
        """
        Reimplemented here because it is faster and probably also more robust to not
        convert to Polygons for this operation and do it directly on bounding boxes.
        """
        return bbox_union(
            BoundingBox(
                left=item.bbox[0],
                bottom=item.bbox[1],
                right=item.bbox[2],
                top=item.bbox[3],
            )
            for item in self.get_items()
            if item.bbox is not None and len(item.bbox) == 4
        ).bbox

    def get_extent(self) -> MultiPolygon:
        bboxes = [box(*item.bbox) for item in self.get_items() if item.bbox is not None]
        union = union_all(bboxes)

        if isinstance(union, MultiPolygon):
            return union

        if union.is_empty:
            return MultiPolygon([])

        if isinstance(union, GeometryCollection):
            # make a MultiPolygon by filtering out all non-polygons
            logger.warning(
                "Dataset version {dataset_version_id} contains non-polygon geometries. "
                "Filtering out those non-polygons.",
                dataset_version_id=self.dataset_version_id,
                union_of_bboxes=union.wkt,
            )
            return MultiPolygon(
                [geom for geom in union.geoms if isinstance(geom, Polygon)]
            )

        logger.warning(
            "Dataset version {dataset_version_id} bounding box union resulted in "
            "unknown geometry type {geometry_type}. Returning empty extent",
            dataset_version_id=self.dataset_version_id,
            geometry_type=type(union),
            union_of_bboxes=union.wkt,
        )

        return MultiPolygon([])
