import datetime
import time
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, Generic, Union, cast

import networkx as nx
import numpy as np
import xarray as xr
from loguru import logger
from networkx import is_directed_acyclic_graph
from odc.geo.geobox import GeoBox
from pyproj import CRS
from rioxarray.exceptions import NoDataInBounds, OneDimensionalRaster
from shapely import MultiPolygon, Polygon, box

from earthscale.constants import XARRAY_CACHE_LEN
from earthscale.datasets.dataset import (
    BandDimensions,
    Dataset,
    DatasetDefinition,
    DatasetMetadata,
    DatasetStatus,
    DatasetType,
    DefinitionType,
    Dimension,
    DimensionInfo,
    DimensionType,
)
from earthscale.datasets.graph import (
    JoinNode,
    get_dset_for_node,
    get_final_node_name,
    validate_graph,
)
from earthscale.datasets.raster._cache import DatasetCache
from earthscale.exceptions import NoDataInSelectionError
from earthscale.types import BBOX, Chunksizes

# Cache to avoid duplicate computations of `.to_xarray()` as that's expensive for large
# datasets
_XARRAY_CACHE = DatasetCache(cache_len=XARRAY_CACHE_LEN)


def _validate_dset(dset: xr.Dataset) -> None:
    assert isinstance(dset, xr.Dataset)
    assert "x" in dset.coords
    assert "y" in dset.coords
    assert dset.rio.crs is not None


class RasterDataset(Generic[DefinitionType], Dataset[DefinitionType]):
    def __init__(
        self,
        name: str,
        explicit_name: bool,
        attributes: dict[str, str] | None,
        graph: nx.DiGraph,
        metadata: DatasetMetadata,
        definition: DefinitionType,
        geobox_callback: Callable[[], GeoBox],
        dataset_id: uuid.UUID | None,
        dataset_version_id: uuid.UUID | None,
    ):
        self._graph = graph
        self._geobox_callback = geobox_callback
        validate_graph(self._graph)

        super().__init__(
            name,
            explicit_name,
            attributes,
            metadata,
            type_=DatasetType.RASTER,
            # Raster datasets are ready by default
            status=DatasetStatus.READY,
            definition=definition,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )

    @property
    def geobox(self) -> GeoBox:
        return self._geobox_callback()

    def get_extent(self) -> MultiPolygon:
        return MultiPolygon([box(*self.geobox.boundingbox)])

    def get_dimension_info(self) -> DimensionInfo:
        raise NotImplementedError

    def join(
        self,
        # Union is required here instead of `|` as that won't work with a string
        others: Union[Sequence["RasterDataset[Any]"], "RasterDataset[Any]"],
        match: "RasterDataset[Any]",
        name: str | None = None,
        metadata: DatasetMetadata | None = None,
    ) -> "RasterDataset[Any]":
        if isinstance(others, RasterDataset):
            others = [others]
        explicit_name = name is not None
        name = name or str(uuid.uuid4())
        new_graph = cast(nx.DiGraph, self._graph.copy())
        join_node_name = f"join_{name}"
        node = JoinNode(
            match_name=match.name,
            output_name=name,
            output_metadata=metadata,
        )
        new_graph.add_node(
            join_node_name,
            node=node,
        )
        # Connect this dataset to the join node
        new_graph.add_edge(
            get_final_node_name(self._graph),
            join_node_name,
        )
        # Connect all other datasets to the join node
        geobox = self.geobox
        for other in others:
            new_graph = nx.union(new_graph, other._graph)
            new_graph.add_edge(
                get_final_node_name(other._graph),
                join_node_name,
            )
            geobox = geobox & other.geobox

        new_attributes = metadata.attributes if metadata is not None else []
        attributes = {
            attr.name: attr.value for attr in self.metadata.attributes + new_attributes
        }
        return RasterDataset(
            name,
            explicit_name,
            attributes,
            new_graph,
            metadata or DatasetMetadata(),
            definition=DatasetDefinition(),
            geobox_callback=lambda: geobox,
            dataset_id=None,
            dataset_version_id=None,
        )

    def to_xarray(  # noqa: C901
        self,
        # The bounding box is assumed to be in EPSG:4326. Might lead to speedups for
        # certain dataset types (e.g. STAC and ImageDataset)
        bbox: BBOX | GeoBox | None = None,
        # Subset of bands to return. Might lead to speedup for certain dataset types
        # (e.g. STAC and ImageDataset)
        bands: Iterable[str] | None = None,
        chunksizes: Chunksizes | None = None,
        memory_limit_megabytes: int = 1024,
        extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]] | None = None,
    ) -> xr.Dataset:
        """
        Loads the dataset into an xarray.Dataset.

        Args:
            bbox:
                Optional. Can be used to only load a subset of the dataset and/or to
                reproject to a different CRS or resolution (defined by a GeoBox).

            bands:
                Optional. Can be used to only load a subset of the bands. For
                multi-dimensional datasets, this can be used to only load a subset of
                the data variables.

            chunksizes:
                Optional. Can be used to set a specific chunk size for the dataset.
                Defaults to the native chunk size of the dataset.

            memory_limit_megabytes:
                Optional. Raises a MemoryLimitExceededError if a reprojection operation
                requested by the `bbox` argument would require more memory than the
                specified limit.

                Set to 0 to disable the check.

            extra_dimension_selector:
                Optional. Used to select a subset of the extra dimensions of the.
                A dict in the form of {dimension_name: value} or {dimension_name:
                (start, end)}. We are using `dset.sel()` under the hood (either with a
                literal value or a slice), so the values should be part of a coordinate
                of the dimension. The information might also be used by implementations
                pre-select the data. E.g. in the case of a STAC datasets, items might
                be pre-selected based on the time, etc.

        Returns:
            The loaded dataset.

        Raises:
            MemoryLimitExceededError:
                If the memory limit is exceeded.

            NoDataInSelectionError:
                If no raster data was found for the selected bbox/dimensions.
        """
        extra_dimension_selector = extra_dimension_selector or {}
        start_time = time.time()
        cached_dset: xr.Dataset | None = None
        if self.dataset_version_id is not None:
            cached_dset = _XARRAY_CACHE.get(
                self.dataset_version_id,
                chunksizes,
                bbox,
                bands,
                extra_dimension_selector,
            )
        if cached_dset is not None:
            logger.debug(
                f"Found xr.Dataset for dataset_version_id '{self.dataset_version_id}', "
                f"bounds '{bbox}', bands '{bands}' and chunksizes '{chunksizes}' in "
                f"the cache, using that"
            )
            dset = cached_dset
        else:
            assert is_directed_acyclic_graph(self._graph)
            final_node_name = get_final_node_name(self._graph)
            dset = get_dset_for_node(
                self._graph,
                final_node_name,
                bbox,
                bands,
                chunksizes,
                memory_limit_megabytes,
                extra_dimension_selector,
            )

        # While the datasets already have information about the `bbox` and `bands`
        # arguments, cropping them again here just to be certain as it should not lead
        # to a performance hit
        if bbox is not None:
            if isinstance(bbox, GeoBox):
                if bbox.crs is None:
                    raise ValueError("Specified GeoBox has no CRS")
                bounds, crs = bbox.boundingbox.bbox, bbox.crs.proj
            else:
                bounds, crs = bbox, CRS.from_epsg(4326)
            try:
                dset = dset.rio.clip_box(*bounds, crs=crs)
            except NoDataInBounds:
                raise NoDataInSelectionError(  # noqa: B904
                    "Selection was empty after clipping by bbox"
                )
            except OneDimensionalRaster:
                # We try with more exact clipping if the above fails because the area
                # is smaller than a pixel
                dset = dset.rio.clip(
                    [box(*bounds, ccw=True)],
                    crs=crs,
                    # All touched is important here to get at leas one pixel
                    all_touched=True,
                )
        if bands is not None:
            dset = dset[bands]

        # Make sure that all "time" values are datetime objects with only dates set
        if "time" in dset.sizes:
            dset["time"] = dset["time"].dt.date.astype(np.datetime64)

        assert isinstance(dset, xr.Dataset)

        _validate_dset(dset)
        if self.dataset_version_id is not None:
            _XARRAY_CACHE.add(
                self.dataset_version_id,
                chunksizes,
                bbox,
                bands,
                dset,
                extra_dimension_selector,
            )
        logger.debug(
            f".to_xarray() for name '{self.name}', dataset_version_id "
            f"'{self.dataset_version_id}', bounds '{bbox}', bands '{bands}' and "
            f"chunksizes '{chunksizes}' took {time.time() - start_time} seconds"
        )
        return dset

    def get_polygon(self, polygon: Polygon | MultiPolygon) -> xr.Dataset:
        dset = self.to_xarray()
        clipped_to_bounds = dset.rio.clip_box(*polygon.bounds)
        clipped = clipped_to_bounds.rio.clip([polygon])
        return cast(xr.Dataset, clipped)

    def get_uncompressed_size_bytes(self) -> int:
        dset = self.to_xarray()
        return dset.nbytes


def get_dimensions_from_dataset(dataset: RasterDataset[Any]) -> DimensionInfo:
    dset = dataset.to_xarray()

    dimension_dict: dict[str, DimensionType] = {}
    band_dimensions: list[BandDimensions] = []
    for band in dset.data_vars:
        dims: list[str] = []

        non_spatial_dims = [
            str(dim) for dim in dset[band].dims if dim not in ["y", "x"]
        ]
        dims.extend(non_spatial_dims)
        new_dims = [dim for dim in non_spatial_dims if dim not in dimension_dict]
        for dim in new_dims:
            # Handle dimensions with no coordinates (just indices)
            dim_values: DimensionType
            if dim not in dset[band].coords:
                dim_values = list(range(dset[band].sizes[dim]))
            else:
                values = dset[band][dim].values
                # Convert datetime64 values to milliseconds since epoch,
                # which is a more portable format
                if np.issubdtype(values.dtype, np.datetime64):
                    dim_values = cast(
                        list[float],
                        (
                            values.astype("datetime64[ns]").astype("int64") / 1_000_000
                        ).tolist(),
                    )
                else:
                    dim_values = cast(list[str], values.tolist())
                # convert to string if inconsistent types
                valid_types = (str, int, float, datetime.datetime)
                if not any(
                    all(isinstance(v, t) for v in dim_values) for t in valid_types
                ):
                    try:
                        dim_values = [str(v) for v in dim_values]
                    except Exception as e:
                        raise ValueError(
                            f"Could not convert dimension values for band '{band}' and "
                            f"dimension '{dim}' to strings"
                        ) from e
            dimension_dict[dim] = dim_values
        band_dimensions.append(
            BandDimensions(band_name=str(band), dimension_names=dims)
        )
    dimensions = [
        Dimension(name=dim, values=values) for dim, values in dimension_dict.items()
    ]
    return DimensionInfo(dimensions=dimensions, band_dimensions=band_dimensions)
