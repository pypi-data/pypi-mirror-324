from typing import Literal, TypedDict

BBOX = tuple[float, float, float, float]


class Chunksizes(TypedDict):
    x: int
    y: int
    time: int


Groupby = (
    Literal["one_plane"] | Literal["time"] | Literal["solar_day"] | Literal["id"] | str
)
