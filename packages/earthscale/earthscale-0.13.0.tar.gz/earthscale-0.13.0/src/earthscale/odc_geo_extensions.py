import math
from typing import cast

from odc.geo import BoundingBox, SomeCRS, SomeResolution
from odc.geo.geobox import GeoBox, GeoboxAnchor
from odc.geo.geom import Geometry, bbox_intersection
from odc.geo.math import maybe_int, shape_  # type: ignore[attr-defined]
from rasterio.warp import transform_bounds


def compute_output_geobox_without_buffering(
    src_geobox: GeoBox,
    dst_crs: SomeCRS,
    dst_resolution: SomeResolution,
    dst_anchor: GeoboxAnchor,
) -> GeoBox:
    """
    This uses rasterio to avoid the buffering that odc.geo.compute_output_geobox does
    which sometimes exceeds the CRS limits.
    """
    non_snapped_output_bounds = cast(
        BoundingBox,
        transform_bounds(
            src_geobox.crs,
            dst_crs,
            *src_geobox.boundingbox,
            densify_pts=101,
        ),
    )
    # Snap to pixel grid
    return GeoBox.from_bbox(
        non_snapped_output_bounds,
        crs=dst_crs,
        resolution=dst_resolution,
        anchor=dst_anchor,
    )


def bbox_contains(
    parent: BoundingBox, child: BoundingBox, abs_tolerance: float = 1e-6
) -> bool:
    if parent.crs != child.crs:
        return False

    return cast(
        bool,
        parent.left - abs_tolerance <= child.left
        and parent.right + abs_tolerance >= child.right
        and parent.bottom - abs_tolerance <= child.bottom
        and parent.top + abs_tolerance >= child.top,
    )


def bbox_intersects(
    a: BoundingBox,
    b: BoundingBox,
) -> bool:
    intersection = bbox_intersection((a, b))
    return intersection.span_x > 0 and intersection.span_y > 0


def geobox_contains(
    parent: GeoBox,
    child: GeoBox,
    abs_tolerance: float = 1e-6,
) -> bool:
    if parent.crs != child.crs:
        return False

    if not bbox_contains(
        parent.extent.boundingbox, child.extent.boundingbox, abs_tolerance
    ):
        return False

    parent_alignment = parent.alignment
    child_alignment = child.alignment

    if (
        abs(parent_alignment.x - child_alignment.x) > abs_tolerance
        or abs(parent_alignment.y - child_alignment.y) > abs_tolerance
    ):
        return False

    parent_resolution = parent.resolution
    child_resolution = child.resolution

    if (
        abs(parent_resolution.x - child_resolution.x) > abs_tolerance
        or abs(parent_resolution.y - child_resolution.y) > abs_tolerance
    ):
        return False

    return True


def geobox_clip(geobox: GeoBox, region: Geometry | BoundingBox) -> GeoBox:
    tol = 0.01
    if isinstance(region, BoundingBox):
        region = region.polygon

    if region.crs is None:
        raise ValueError("Must supply georeferenced region")

    if geobox.crs is None:
        raise ValueError("Must supply georeferenced geobox")

    self_pix_bbox = BoundingBox(0, 0, geobox.shape[1], geobox.shape[0], crs=None)
    if region.crs != geobox.crs:
        region = region.to_crs(geobox.crs)

    region_local_bbox = region.boundingbox
    region_pix_bbox = region.transform(geobox.wld2pix, crs=None).boundingbox

    intersection = bbox_intersection((self_pix_bbox, region_pix_bbox))

    x0, y0, x1, y1 = intersection

    intersection = BoundingBox(
        math.ceil(maybe_int(x0, tol)),
        math.ceil(maybe_int(y0, tol)),
        math.floor(maybe_int(x1, tol)),
        math.floor(maybe_int(y1, tol)),
        crs=geobox.crs,
    )

    nx, ny = (int(span) for span in (intersection.span_x, intersection.span_y))
    tx, ty, *_ = intersection.bbox
    intersection_transform = geobox.translate_pix(tx, ty).affine

    intersection_geobox = GeoBox(shape_((ny, nx)), intersection_transform, geobox.crs)

    assert intersection_geobox.shape[0] <= geobox.shape[0]
    assert intersection_geobox.shape[1] <= geobox.shape[1]
    assert intersection_geobox.transform.xoff >= geobox.transform.xoff
    # y offset is top-left, thats why this feels weird
    assert intersection_geobox.transform.yoff <= geobox.transform.yoff
    assert bbox_contains(region_local_bbox, intersection_geobox.extent.boundingbox)

    return intersection_geobox


def clip_geobox(geobox: GeoBox, region: Geometry | BoundingBox) -> GeoBox:
    tol = 0.01
    if isinstance(region, BoundingBox):
        region = region.polygon

    if region.crs is None:
        raise ValueError("Must supply georeferenced region")

    if geobox.crs is None:
        raise ValueError("Must supply georeferenced geobox")

    self_pix_bbox = BoundingBox(0, 0, geobox.shape[1], geobox.shape[0], crs=None)
    if region.crs != geobox.crs:
        region = region.to_crs(geobox.crs)

    region_local_bbox = region.boundingbox
    region_pix_bbox = region.transform(geobox.wld2pix, crs=None).boundingbox

    intersection = bbox_intersection((self_pix_bbox, region_pix_bbox))

    x0, y0, x1, y1 = intersection

    intersection = BoundingBox(
        math.ceil(maybe_int(x0, tol)),
        math.ceil(maybe_int(y0, tol)),
        math.floor(maybe_int(x1, tol)),
        math.floor(maybe_int(y1, tol)),
        crs=geobox.crs,
    )

    nx, ny = (int(span) for span in (intersection.span_x, intersection.span_y))
    tx, ty, *_ = intersection.bbox
    intersection_transform = geobox.translate_pix(tx, ty).affine

    intersection_geobox = GeoBox(shape_((ny, nx)), intersection_transform, geobox.crs)

    assert intersection_geobox.shape[0] <= geobox.shape[0]
    assert intersection_geobox.shape[1] <= geobox.shape[1]
    assert intersection_geobox.transform.xoff >= geobox.transform.xoff
    # y offset is top-left, thats why this feels weird
    assert intersection_geobox.transform.yoff <= geobox.transform.yoff
    assert bbox_contains(region_local_bbox, intersection_geobox.extent.boundingbox)

    return intersection_geobox
