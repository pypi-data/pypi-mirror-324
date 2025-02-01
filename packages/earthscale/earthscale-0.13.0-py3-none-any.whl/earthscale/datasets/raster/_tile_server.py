import uuid
from collections.abc import Iterable, Mapping
from typing import Any

import contextily as ctx
import numpy as np
import xarray as xr
from odc.geo.geobox import GeoBox
from rasterio.transform import from_bounds

from earthscale.datasets.dataset import (
    DatasetDefinition,
    DatasetMetadata,
    DimensionInfo,
)
from earthscale.datasets.graph import create_source_graph
from earthscale.datasets.raster import RasterDataset
from earthscale.types import BBOX, Chunksizes


class TileServerDatasetDefinition(DatasetDefinition):
    url: str


class TileServerDataset(RasterDataset[TileServerDatasetDefinition]):
    """
    Load data from a tile server.

    Args:
        url (str): The URL of the tile server with x, y, z placeholders, e.g.
            `https://server.com/tiles/{z}/{x}/{y}.png`.
        name (str, optional): The name of the dataset. Defaults to a random UUID.
            If explicitly given, the dataset will be visible in the Earthscale platform.
    """

    def __init__(
        self,
        url: str,
        name: str | None = None,
        attributes: dict[str, str] | None = None,
        metadata: DatasetMetadata | None = None,
        definition: TileServerDatasetDefinition | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
    ):
        explicit_name = name is not None
        name = name or str(uuid.uuid4())

        definition = definition or TileServerDatasetDefinition(url=url)

        if metadata is None:
            metadata = DatasetMetadata()
        metadata.tileserver_url = url
        metadata.supports_custom_viz = False

        super().__init__(
            name=name,
            explicit_name=explicit_name,
            attributes=attributes,
            graph=create_source_graph(
                f"load_tileserver_dataset_{name}",
                name,
                metadata,
                self._load,
            ),
            metadata=metadata,
            geobox_callback=self._geobox_callback,
            definition=definition,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    def _load(
        self,
        bbox: BBOX | GeoBox | None,
        bands: Iterable[str] | None,
        _chunksizes: Chunksizes | None,
        _memory_limit_megabytes: int,
        extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
    ) -> xr.Dataset:
        if isinstance(bbox, GeoBox):
            raise ValueError("GeoBox is not supported for loading TileServerDataset")
        # Define the bounds, either from bbox or default to global extent
        if bbox is not None:
            # bbox is in (left, bottom, right, top) in WGS84
            left, bottom, right, top = bbox
        else:
            # Default to global extent in WGS84
            left, bottom, right, top = (-180, -85.0511, 180, 85.0511)

        # Fetch the image
        img, extent = ctx.bounds2img(
            left,
            bottom,
            right,
            top,
            ll=True,
            zoom="auto",
            source=self.definition.url,
        )

        # img is an array of shape (height, width, bands)
        # extent is (left, bottom, right, top) in Web Mercator (EPSG:3857)

        # Create coordinates
        x = np.linspace(extent[0], extent[1], img.shape[1])
        y = np.linspace(extent[3], extent[2], img.shape[0])

        # Create dataset with x and y coordinates
        dset = xr.Dataset(
            coords={
                "x": ("x", x),
                "y": ("y", y),
            }
        )

        # Set band names and create data variables
        num_bands = img.shape[2]
        if num_bands == 3:
            band_names = ["red", "green", "blue"]
        elif num_bands == 4:
            band_names = ["red", "green", "blue", "alpha"]
        else:
            band_names = [f"band_{i + 1}" for i in range(num_bands)]

        for i, band_name in enumerate(band_names):
            dset[band_name] = xr.DataArray(
                img[:, :, i],
                dims=("y", "x"),
                coords={"x": x, "y": y},
            )

        # Set CRS
        dset.rio.write_crs("EPSG:3857", inplace=True)

        if bands is not None:
            dset = dset[list(bands)]

        return dset

    def _geobox_callback(self) -> GeoBox:
        # Default to global extent in Web Mercator (EPSG:3857)
        left, bottom, right, top = (
            -20037508.34,
            -20037508.34,
            20037508.34,
            20037508.34,
        )
        width, height = 256, 256  # Default tile size
        crs = "EPSG:3857"

        transform = from_bounds(
            west=left,
            south=bottom,
            east=right,
            north=top,
            width=width,
            height=height,
        )
        geobox = GeoBox((height, width), transform, crs)
        return geobox

    def get_dimension_info(self) -> DimensionInfo:
        return DimensionInfo(dimensions=[], band_dimensions=[])

    def get_uncompressed_size_bytes(self) -> int:
        return 0
