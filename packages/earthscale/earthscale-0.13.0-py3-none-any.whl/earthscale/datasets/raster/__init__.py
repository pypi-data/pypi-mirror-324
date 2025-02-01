from earthscale.datasets.dataset import (
    registry,
)

# This try-expect purely exists to avoid import re-ordering here
try:
    # Base needs to be imported first
    from earthscale.datasets.raster._base import RasterDataset
    from earthscale.datasets.raster._cache import CacheEntry, DatasetCache

    # Datasets
    from earthscale.datasets.raster._earth_engine import (
        EarthEngineDataset,
        EarthEngineDatasetDefinition,
    )
    from earthscale.datasets.raster._image import ImageDataset, ImageDatasetDefinition
    from earthscale.datasets.raster._stac import STACDataset, STACDatasetDefinition
    from earthscale.datasets.raster._tile_server import (
        TileServerDataset,
        TileServerDatasetDefinition,
    )
    from earthscale.datasets.raster._zarr import ZarrDataset, ZarrDatasetDefinition
except Exception as e:
    raise e


registry.register_class("ZarrDataset", ZarrDataset)
registry.register_class("STACDataset", STACDataset)
registry.register_class("ImageDataset", ImageDataset)
registry.register_class("EarthEngineDataset", EarthEngineDataset)
registry.register_class("TileServerDataset", TileServerDataset)


__all__ = [
    "CacheEntry",
    "DatasetCache",
    "EarthEngineDataset",
    "EarthEngineDatasetDefinition",
    "ImageDataset",
    "ImageDatasetDefinition",
    "RasterDataset",
    "STACDataset",
    "STACDatasetDefinition",
    "TileServerDataset",
    "TileServerDatasetDefinition",
    "ZarrDataset",
    "ZarrDatasetDefinition",
]
