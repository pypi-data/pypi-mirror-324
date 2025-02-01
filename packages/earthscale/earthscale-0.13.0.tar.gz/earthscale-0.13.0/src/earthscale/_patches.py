from typing import cast

import fsspec
import odc.geo.xr
import odc.stac
import pyproj
import rasterio
from odc.geo import BoundingBox, Geometry, SomeCRS
from odc.geo.geobox import GeoBox, GeoBoxBase, GeoboxTiles

from earthscale.raster_utils import (
    detect_crs_from_cf_convention_tags,
)


def _patched_geo_box_from_rio(rdr: rasterio.DatasetReader) -> GeoBox:
    """
    This overrides the GeoBox.from_rio method to use the CF tags to detect the CRS
    """
    crs = rdr.crs
    if crs is None:
        crs = detect_crs_from_cf_convention_tags(rdr.tags())
    return GeoBox(
        shape=rdr.shape,
        affine=rdr.transform,
        crs=crs,
    )


GeoBox.from_rio = _patched_geo_box_from_rio  # type: ignore


def _patched_geo_box_footprint(
    self: GeoBoxBase,
    crs: SomeCRS,
    buffer: float = 0,
    npoints: int = 100,
) -> Geometry:
    """
    This clips to WebMercator bounds if necessary to avoid errors seen in production.
    """
    assert self.crs is not None
    ext: Geometry = self.extent
    if buffer != 0:
        buffer = buffer * max(*self.resolution.xy)
        ext = ext.buffer(buffer)

    if not isinstance(crs, pyproj.CRS):
        crs = pyproj.CRS(crs)

    if self.crs.geographic and crs.to_epsg() == 3857:
        # clip to web mercator bounds
        ext_bounds = ext.boundingbox
        ext_bounds = BoundingBox(
            left=max(-180.0, ext_bounds.left),
            bottom=max(-85.0511, ext_bounds.bottom),
            right=min(180.0, ext_bounds.right),
            top=min(85.0511, ext_bounds.top),
        )
        ext = odc.geo.geom.box(
            left=ext_bounds.left,
            bottom=ext_bounds.bottom,
            right=ext_bounds.right,
            top=ext_bounds.top,
            crs=ext.crs,
        )

    return ext.to_crs(crs, resolution=self._reproject_resolution(npoints)).dropna()


GeoBoxBase.footprint = _patched_geo_box_footprint  # type: ignore


def _fixed_grid_intersect(
    self: GeoboxTiles,
    src: GeoboxTiles,
) -> dict[
    tuple[int, int],
    list[tuple[int, int]],
]:
    """
    Figure out tile to tile overlap graph between two grids.

    For every tile in this :py:class:`GeoboxTiles` find every tile in ``other`` that
    intersects with this ``tile``.
    """
    A = self._check_linear(src)
    if A is not None:
        return self._grid_intersect_linear(src, A)

    if src.base.crs == self.base.crs:
        src_footprint = src.base.extent
    else:
        # compute "robust" source footprint in CRS of self via espg:4326
        src_footprint = (
            (src.base.footprint(4326) & self.base.footprint(4326))
            .to_crs(self.base.crs)
            .simplify(tolerance=1e-6)
        )

    xy_chunks_with_data = list(self.tiles(src_footprint))
    deps: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for idx in xy_chunks_with_data:
        geobox = self[idx]
        deps[idx] = list(src.tiles(geobox.extent))

    return deps


GeoboxTiles.grid_intersect = _fixed_grid_intersect  # type: ignore[method-assign]


def _repr_fsmap(self: fsspec.FSMap) -> str:
    return cast(str, self.root)


fsspec.FSMap.__repr__ = _repr_fsmap
