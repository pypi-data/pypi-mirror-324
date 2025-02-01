import uuid
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

import xarray as xr
from odc.geo import BoundingBox
from odc.geo.geobox import GeoBox

from earthscale.odc_geo_extensions import bbox_contains, geobox_contains
from earthscale.types import BBOX, Chunksizes


class CacheEntry:
    def __init__(
        self,
        dset: xr.Dataset,
        bbox: BBOX | GeoBox | None,
        bands: Iterable[str] | None,
        chunksizes: Chunksizes | None,
        extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
    ):
        self.dset = dset
        self.bbox = bbox
        self.bands: tuple[str, ...] | None = tuple(bands) if bands is not None else None
        self.chunksizes = chunksizes
        self.extra_dimension_selector = extra_dimension_selector


class DatasetCache:
    """Geo-aware cache for datasets, checking to see if we already
    have a dataset with the same bounding box and bands.

    Evicts the oldest entries first
    """

    def __init__(self, cache_len: int = 10):
        assert cache_len > 0
        self.cache_len = cache_len
        self.cache: dict[uuid.UUID, list[CacheEntry]] = defaultdict(list)
        self.most_recent_keys: list[uuid.UUID] = []

    def _total_length(self) -> int:
        return sum(len(v) for v in self.cache.values())

    def add(
        self,
        dataset_version_id: uuid.UUID,
        chunksizes: Chunksizes | None,
        bbox: BBOX | GeoBox | None,
        bands: Iterable[str] | None,
        dset: xr.Dataset,
        extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
    ) -> None:
        entry = CacheEntry(dset, bbox, bands, chunksizes, extra_dimension_selector)
        if dataset_version_id not in self.cache:
            self.cache[dataset_version_id] = []
        self.cache[dataset_version_id].append(entry)
        self.most_recent_keys.append(dataset_version_id)
        if self._total_length() > self.cache_len:
            oldest_key = self.most_recent_keys.pop(0)
            if len(self.cache[oldest_key]) > 0:
                self.cache[oldest_key].pop(0)
            else:
                # if the key no longer has any entries, remove it from the cache
                self.most_recent_keys = [
                    k for k in self.most_recent_keys if k != oldest_key
                ]

    def get(  # noqa: C901
        self,
        dataset_version_id: uuid.UUID,
        chunksizes: Chunksizes | None,
        bbox: BBOX | GeoBox | None,
        bands: Iterable[str] | None,
        extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
    ) -> xr.Dataset | None:
        entries = self.cache[dataset_version_id]
        self.most_recent_keys.append(dataset_version_id)
        for entry in entries:
            if chunksizes != entry.chunksizes:
                continue

            if entry.bands is not None:
                if bands is None:
                    continue
                if not all(band in entry.bands for band in bands):
                    continue

            if (
                len(extra_dimension_selector) > 0
                and entry.extra_dimension_selector != extra_dimension_selector
            ):
                continue

            if isinstance(bbox, GeoBox) and isinstance(entry.bbox, GeoBox):
                if geobox_contains(entry.bbox, bbox):
                    return entry.dset
                continue

            if entry.bbox is None and not isinstance(bbox, GeoBox):
                return entry.dset

            if (
                isinstance(bbox, tuple)
                and isinstance(entry.bbox, tuple)
                and bbox_contains(
                    parent=BoundingBox(*entry.bbox, crs=None),
                    child=BoundingBox(*bbox, crs=None),
                )
            ):
                return entry.dset

        return None
