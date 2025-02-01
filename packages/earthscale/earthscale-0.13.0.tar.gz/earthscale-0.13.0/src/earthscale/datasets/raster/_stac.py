import uuid
from collections.abc import Iterable, Mapping
from typing import Any

import xarray as xr
from odc.geo.geobox import GeoBox
from pystac import Item
from stac_pydantic.item import Item as PydanticItem

from earthscale._stac_utils import convert_stac_items_to_geobox, load_stac_dataset
from earthscale.datasets.dataset import DatasetDefinition, DatasetMetadata
from earthscale.datasets.graph import create_source_graph
from earthscale.datasets.raster import RasterDataset
from earthscale.types import BBOX, Chunksizes, Groupby


class STACDatasetDefinition(DatasetDefinition):
    items: list[PydanticItem]
    bands: list[str] | None
    groupby: Groupby | None
    kw_args: dict[str, Any] | None


class STACDataset(RasterDataset[STACDatasetDefinition]):
    """Spatio-Temporal Asset Catalog (STAC) based dataset

    Args:
        items:
            Items to build the dataset from. We allow passing in serialized stac items
            (dicts) as well.
            If no explicit geobox is passed in, the geobox will be determined from the
            items. In this case, the proj extension to the STAC item is required. When
            using rio-stac's `create_stac_item` function, this can be achieved by
            passing in the `with_proj=True` argument.

        bands:
            List of bands to load. Defaults to all bands

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

        name:
            Name of the dataset. Defaults to a random UUID. If explicitly given,
            The dataset will be visible in the Earthscale platform

        metadata:
            Dataset Metadata. Defaults to None.

        kwargs:
            Additional keyword arguments to pass to
            [`odc.stac.load`](https://odc-stac.readthedocs.io/en/latest/_api/odc.stac.load.html)
            Only serializable arguments can be passed to STAC.
    """

    def __init__(
        self,
        items: list[Item | dict[str, Any]],
        bands: list[str] | None = None,
        groupby: Groupby | None = "one_plane",
        name: str | None = None,
        attributes: dict[str, str] | None = None,
        metadata: DatasetMetadata | None = None,
        dataset_id: uuid.UUID | None = None,
        dataset_version_id: uuid.UUID | None = None,
        **kwargs: Any | None,
    ):
        parsed_items = [
            Item.from_dict(item) if not isinstance(item, Item) else item
            for item in items
        ]

        metadata = metadata or DatasetMetadata()
        explicit_name = name is not None
        name = name or str(uuid.uuid4())
        geobox = convert_stac_items_to_geobox(
            tuple(parsed_items),
            tuple(bands) if bands else None,
            **kwargs,
        )

        definition = STACDatasetDefinition(
            items=[PydanticItem(**item.to_dict()) for item in parsed_items],
            bands=bands,
            groupby=groupby,
            kw_args=kwargs,
        )

        def _load_stac_dataset_wrapper(
            bbox: BBOX | GeoBox | None,
            bands_selection: Iterable[str] | None,
            chunksizes: Chunksizes | None,
            _memory_limit_megabytes: int,
            extra_dimension_selector: Mapping[str, Any | tuple[Any, Any]],
        ) -> xr.Dataset:
            # If a particular `to_xarray` call requests all bands, but
            # the dataset was created with a subset of bands, we need
            # to respect that and not load all bands from the STAC
            # items.
            if bands and not bands_selection:
                bands_selection = bands
            return load_stac_dataset(
                items=parsed_items,
                bands=bands_selection,
                groupby=groupby,
                full_geobox=geobox,
                bbox=bbox,
                chunksizes=chunksizes,
                extra_dimension_selector=extra_dimension_selector,
                **kwargs,
            )

        super().__init__(
            name=name or str(uuid.uuid4()),
            explicit_name=explicit_name,
            attributes=attributes,
            graph=create_source_graph(
                f"load_file_dataset_{name}", name, metadata, _load_stac_dataset_wrapper
            ),
            metadata=metadata,
            geobox_callback=lambda: geobox,
            definition=definition,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
        )
