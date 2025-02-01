import datetime
import functools
import uuid
from collections.abc import Callable
from contextlib import suppress
from typing import Any, TypeVar, cast

import ee
import numpy as np
import requests
import xarray as xr
from affine import Affine
from loguru import logger
from odc.geo import Resolution
from odc.geo.geobox import GeoBox
from pyproj import CRS, Transformer
from pyproj.enums import TransformDirection
from shapely import Polygon

from earthscale.constants import (
    METERS_PER_DEGREE,
)
from earthscale.datasets._earthengine import parse_earth_engine_stac_to_earthscale
from earthscale.datasets.dataset import (
    BandDimensions,
    DatasetDefinition,
    DatasetMetadata,
    Dimension,
    DimensionInfo,
)
from earthscale.datasets.graph import (
    create_source_graph,
)
from earthscale.datasets.raster import RasterDataset
from earthscale.exceptions import (
    CannotConvertEarthEngineToXarrayError,
    UnsupportedRasterFormatError,
)
from earthscale.proj_utils import crs_from_str
from earthscale.utils import (
    generate_filter_date_range,
)


def _get_crs_from_ee_projection(projection: dict[str, Any]) -> CRS:
    if "crs" in projection:
        crs = crs_from_str(projection["crs"])
    elif "wkt" in projection:
        crs = CRS.from_string(projection["wkt"])
    else:
        raise ValueError("Could not determine CRS from EE image")
    return crs


def _get_approx_m_per_pixel_at_point(
    crs: CRS, crs_transform: Affine, point_4326: tuple[float, float]
) -> float:
    to_4326 = Transformer.from_crs(crs, CRS.from_epsg(4326), always_xy=True)
    c_local = to_4326.transform(
        *point_4326,
        direction=TransformDirection.INVERSE,
    )
    points_local = np.array(
        [
            [c_local[0], c_local[0] + crs_transform.a, c_local[0]],
            [c_local[1], c_local[1], c_local[1] + crs_transform.e],
        ],
        np.float64,
    )
    points_4326 = np.vstack(to_4326.transform(points_local[0], points_local[1]))

    local_aeqd = CRS(proj="aeqd", lon_0=points_4326[0][0], lat_0=points_4326[1][0])
    to_local_aeqd = Transformer.from_crs(
        CRS.from_epsg(4326), local_aeqd, always_xy=True
    )
    points_local_aeqd = np.vstack(
        to_local_aeqd.transform(points_4326[0], points_4326[1])
    ).T

    res_x = np.linalg.norm(points_local_aeqd[0] - points_local_aeqd[1])
    res_y = np.linalg.norm(points_local_aeqd[0] - points_local_aeqd[2])
    return cast(float, (res_x + res_y) / 2)


def _load_geobox_from_ee_image_collection(
    image_collection: ee.ImageCollection,
) -> GeoBox:
    error_margin_meters = 0.5
    error_margin = ee.ErrorMargin(error_margin_meters, "meters")
    limit = 10_000
    number_of_images = image_collection.limit(limit).size().getInfo()

    # We return all of our geoboxes as WGS84
    crs_4326 = CRS.from_string("EPSG:4326")
    first_image = image_collection.first()
    # In case we've got exactly one image, we can perfectly reconstruct the geobox
    if number_of_images == 1:
        bbox = Polygon(
            first_image.geometry(error_margin)
            .bounds(error_margin)
            .getInfo()["coordinates"][0]
        ).bounds
    # In case we've got <10_000 images in the collection, we can still compute the
    # bounds and the merged CRS will be WGS84. 10_000 here was determined empirically.
    # If the number is too high, `.geometry()` will fail due to a memory error on EE.
    # We'll get the resolution from the first image, assuming all other images have
    # the same
    elif number_of_images < limit:
        bbox = Polygon(
            image_collection.geometry(error_margin)
            .bounds(error_margin)
            .getInfo()["coordinates"][0]
        ).bounds
    # If both of the above fail, we fall back to a "whole world geobox" using the
    # resolution of the first image
    else:
        logger.warning(
            "The provided EE image collection is too large to compute the geobox. "
            "Falling back to a whole world bounding box"
        )
        bbox = (-180, -90, 180, 90)

    highest_res_band = find_ee_image_highest_resolution_from_bands(first_image, bbox)
    if highest_res_band is None:
        raise ValueError("First image has no bands, cannot determine geobox")
    resolution_m = highest_res_band[-1]
    resolution_4326 = resolution_m / METERS_PER_DEGREE
    geobox = GeoBox.from_bbox(
        bbox=bbox, crs=crs_4326, resolution=Resolution(resolution_4326)
    )
    return geobox


def find_ee_image_highest_resolution_from_bands(
    image: ee.Image,
    image_bbox_4326: tuple[float, float, float, float],
) -> tuple[str, CRS, Affine, float] | None:
    """
    Returns band_name, crs, affine, and meters_per_pixel of the band with the highest
    resolution.
    """
    image_center_4326 = (
        (image_bbox_4326[0] + image_bbox_4326[2]) / 2,
        (image_bbox_4326[1] + image_bbox_4326[3]) / 2,
    )
    band_metadata = image.getInfo()["bands"]
    if not band_metadata:
        return None

    bands_with_crs_and_res: list[tuple[str, CRS, Affine, float]] = []

    for band_meta in band_metadata:
        band_crs = _get_crs_from_ee_projection(band_meta)
        band_transform = Affine(*band_meta["crs_transform"])
        meters_per_pixel = _get_approx_m_per_pixel_at_point(
            band_crs, band_transform, image_center_4326
        )
        bands_with_crs_and_res.append(
            (band_meta["id"], band_crs, band_transform, meters_per_pixel)
        )
    return min(bands_with_crs_and_res, key=lambda x: x[-1])


def _fail_when_loading_ee() -> xr.Dataset:
    raise CannotConvertEarthEngineToXarrayError(
        "Due to limitations in the metadata that Earth Engine provides on "
        "ImageCollections, we cannot load this dataset as an xarray Dataset."
    )


class EarthEngineDatasetDefinition(DatasetDefinition):
    # JSON serialized version of the ee.ImageCollection object
    image_collection: dict[str, Any]
    quality_band: str | None
    viz_params: dict[str, Any] | None


CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def wrap_known_earthengine_errors(func: CallableT) -> CallableT:
    @functools.wraps(func)
    def _wrap(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ee.EEException as e:
            if len(e.args) > 0 and "Image.projection" in e.args[0]:
                raise UnsupportedRasterFormatError(*e.args) from None
            raise e

    return cast(CallableT, _wrap)


def _convert_ee_viz_params(ee_viz: dict[str, Any]) -> dict[str, Any]:
    result = {}
    for key, value in ee_viz.items():
        if isinstance(value, list):
            result[key] = ",".join(map(str, value))
        else:
            result[key] = str(value)
    return result


class EarthEngineDataset(RasterDataset[EarthEngineDatasetDefinition]):
    """
    Load data from Earth Engine.

    Args:
        image_collection:
            Either an ee.ImageCollection object or JSON dict of the image collection
        quality_band:
            The band used to determine the pixel ordering in the mosaic creation. Please
            refer to the [Earth-engine docs](https://developers.google.com/earth-engine/apidocs/ee-imagecollection-qualitymosaic)
            for an example.
        viz_params:
            Visualization parameters for the mosaic. Please refer to the docs on
            [Image Visualization](https://developers.google.com/earth-engine/guides/image_visualization)
            on what's possible here.

            An example here would be:
            ```python
            viz_params = {
                "bands": ["B4", "B3", "B2"],
                "min": [0, 0, 0],
                "max": [0.3, 0.3, 0.3]
            }
            ```

        name:
            The name of the dataset. Defaults to a random UUID. If explicitly given, the
            dataset will be visible in the Earthscale platform.
    """

    @staticmethod
    def fetch_earth_engine_catalog_stac(earth_engine_id: str) -> dict[str, Any] | None:
        base_url = "https://storage.googleapis.com/earthengine-stac/catalog/"
        if earth_engine_id.startswith("projects"):
            base_catalog = earth_engine_id.split("/")[1]
        else:
            base_catalog = earth_engine_id.split("/")[0]
        escaped_name = earth_engine_id.replace("/", "_")
        url = f"{base_url}{base_catalog}/{escaped_name}.json"

        with requests.get(url) as response:
            if response.status_code != 200:
                logger.warning(
                    "Failed to fetch Earth Engine catalog STAC for id "
                    "'{earth_engine_id}' from URL {url}. Status code: {status_code}",
                    earth_engine_id,
                    url,
                    response.status_code,
                )
                return None
            return cast(dict[str, Any], response.json())

    @staticmethod
    def from_earth_engine_catalog(
        earth_engine_id: str,
        custom_name: str | None = None,
        preprocessing_function: Callable[
            [ee.ImageCollection, DatasetMetadata], ee.ImageCollection
        ]
        | None = None,
    ) -> "EarthEngineDataset":
        """
        Load an Earth Engine dataset from the Earth Engine catalog.

        The id can be found in the "Collection Snippet" field.
        Example value: "COPERNICUS/DEM/GLO30"

        """
        ds_stac = EarthEngineDataset.fetch_earth_engine_catalog_stac(earth_engine_id)
        if ds_stac is None:
            raise ValueError(
                "Could not fetch Earth Engine catalog STAC, check if the "
                "given ID '{earth_engine_id}' exists"
            )

        ee_type = ds_stac.get("gee:type")
        if not ee_type:
            raise ValueError("Could not determine the type of the Earth Engine dataset")

        if ee_type == "image":
            ee_coll = ee.ImageCollection([ee.Image(earth_engine_id)])
        elif ee_type == "image_collection":
            ee_coll = ee.ImageCollection(earth_engine_id)
        else:
            raise ValueError(f"Dataset has unsupported type: {ee_type}")

        metadata = parse_earth_engine_stac_to_earthscale(ds_stac)
        if preprocessing_function is not None:
            ee_coll = preprocessing_function(ee_coll, metadata)

        return EarthEngineDataset(
            image_collection=ee_coll,
            name=earth_engine_id if custom_name is None else custom_name,
            metadata=metadata,
        )

    @wrap_known_earthengine_errors
    def __init__(
        self,
        image_collection: ee.ImageCollection | dict[str, Any],
        quality_band: str | None = None,
        viz_params: dict[str, Any] | None = None,
        attributes: dict[str, str] | None = None,
        name: str | None = None,
        metadata: DatasetMetadata | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
    ):
        if isinstance(image_collection, dict):
            image_collection = ee.ImageCollection(
                ee.deserializer.decode(image_collection)
            )
        if image_collection.limit(1).size().getInfo() == 0:
            raise ValueError("The provided image collection is empty")
        explicit_name = name is not None
        name = name or str(uuid.uuid4())

        definition = EarthEngineDatasetDefinition(
            image_collection=ee.serializer.encode(image_collection),
            quality_band=quality_band,
            viz_params=viz_params,
        )

        self.quality_band = quality_band

        if quality_band is None:
            image = image_collection.mosaic()
        else:
            image = image_collection.qualityMosaic(quality_band)

        self.image = image
        self.image_collection = image_collection

        # TODO: remove these?
        if viz_params is None:
            viz_params = {}
        else:
            # Earthengine expects viz params to be a comma-separated string
            viz_params = {
                k: ",".join(map(str, v)) if isinstance(v, list) else str(v)
                for k, v in viz_params.items()
            }
        self.viz_params = viz_params

        if metadata is None:
            metadata = DatasetMetadata()
        metadata.supports_custom_viz = False

        @wrap_known_earthengine_errors
        def _load_geobox() -> GeoBox:
            logger.info(
                "Loading geobox from Earth Engine for dataset "
                "{dataset_id} ({dataset_name}) ee_id: {earth_engine_id}",
                dataset_id=dataset_id,
                dataset_name=name,
                earth_engine_id=metadata.source_id,
            )
            return _load_geobox_from_ee_image_collection(image_collection)

        super().__init__(
            name=name,
            explicit_name=explicit_name,
            attributes=attributes,
            graph=create_source_graph(
                f"load_earthengine_dataset_{name}",
                name,
                metadata,
                lambda _a, _b, _c, _d, _e: _fail_when_loading_ee(),
            ),
            metadata=metadata,
            definition=definition,
            geobox_callback=_load_geobox,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    def get_filtered_collection(
        self,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
        geometry: ee.Geometry | None = None,
    ) -> ee.ImageCollection:
        coll = self.image_collection
        if start_time is not None or end_time is not None:
            if start_time is None and end_time is not None:
                start_time = end_time - datetime.timedelta(milliseconds=1)
            if end_time is None and start_time is not None:
                end_time = start_time + datetime.timedelta(milliseconds=1)
            coll = coll.filter(
                ee.Filter.date(
                    ee.Date(start_time),
                    ee.Date(end_time),
                )
            )
        if geometry is not None:
            coll = coll.filterBounds(geometry)
        return coll

    def get_mosaic(
        self,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
    ) -> ee.Image | None:
        coll = self.get_filtered_collection(start_time, end_time)
        # check if the collection is empty after filtering
        # -> in this case we cannot create a map and have to return None
        if coll.limit(1).size().getInfo() == 0:
            return None

        if self.quality_band is None or self.quality_band not in self.metadata.bands:
            image = coll.mosaic()
        else:
            image = coll.qualityMosaic(self.quality_band)
        return image

    def get_tileserver_url(
        self,
        ee_viz_params: dict[str, Any] | None = None,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
    ) -> str | None:
        image = self.get_mosaic(start_time, end_time)
        if image is None:
            return None

        get_map_id_params = {"image": image}
        if ee_viz_params is not None:
            get_map_id_params |= _convert_ee_viz_params(ee_viz_params)

        url = cast(
            str,
            ee.data.getMapId(get_map_id_params)["tile_fetcher"].url_format,
        )
        return url

    def get_dimension_info(self) -> DimensionInfo:
        """
        Auto-guesses useful dates from the time range of the metadata.

        Logic:
        if we have > 10 years, use years,
        if we just have one year, use months,
        if we have less than half a year use weeks
        if we have less than a month use days

        TODO: figure out how temporal_resolution should play into this
        """
        meta: DatasetMetadata = self.metadata
        if meta.temporal_extent is None:
            return DimensionInfo(dimensions=[], band_dimensions=[])
        start, end = meta.temporal_extent
        times = generate_filter_date_range(start, end)
        dim = Dimension(name="time", values=times)
        band_dimensions = [
            BandDimensions(band_name=band, dimension_names=["time"])
            for band in meta.bands
        ]
        return DimensionInfo(dimensions=[dim], band_dimensions=band_dimensions)

    @staticmethod
    def load_visualizations_from_stac(earth_engine_id: str) -> dict[str, Any]:
        ds_stac = EarthEngineDataset.fetch_earth_engine_catalog_stac(earth_engine_id)

        visualizations: dict[str, Any] = {}
        if ds_stac is None:
            logger.warning(
                "Could not fetch Earth Engine catalog STAC for dataset "
                f"with Earth Engine ID '{earth_engine_id}'"
            )
            return visualizations
        try:
            ee_visualizations = ds_stac["summaries"]["gee:visualizations"]
            for vis in ee_visualizations:
                # just skip the ones we cannot support for now
                with suppress(KeyError):
                    vis_name = vis["display_name"]
                    visualizations[vis_name] = vis["image_visualization"]["band_vis"]
        except KeyError:
            logger.warning(
                "Could not find visualizations in Earth Engine catalog for dataset "
                f"with Earth Engine ID '{earth_engine_id}'"
            )
        return visualizations

    def get_uncompressed_size_bytes(self) -> int:
        return 0
