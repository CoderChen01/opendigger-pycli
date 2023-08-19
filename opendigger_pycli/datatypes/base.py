from dataclasses import dataclass
from typing import Generic, List, NamedTuple, TypedDict, TypeVar

T = TypeVar("T")
S = TypeVar("S")


@dataclass
class BaseData(Generic[T]):
    year: int
    month: int
    value: T


class NameAndValue(NamedTuple):
    name: str
    value: float


class NameNameAndValue(NamedTuple):
    name0: str
    name1: str
    value: float


AvgData = BaseData[float]
LevelData = BaseData[List[int]]
QuantileData = BaseData[float]


class NonTrivialMetricDict(TypedDict):
    avg: List[AvgData]
    levels: List[LevelData]
    quantile0: List[QuantileData]
    quantile1: List[QuantileData]
    quantile2: List[QuantileData]
    quantile3: List[QuantileData]
    quantile4: List[QuantileData]


@dataclass
class BaseNetworkData(Generic[T, S]):
    nodes: List[T]
    edges: List[S]
