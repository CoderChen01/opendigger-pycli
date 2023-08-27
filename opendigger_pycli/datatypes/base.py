import typing as t
from dataclasses import dataclass
from typing import Generic, List, NamedTuple, TypedDict, TypeVar


T = TypeVar("T")
S = TypeVar("S")

TRIVIAL_INDICATOR_DATA = "trivial_indicator_data"
NON_TRIVIAL_INDICATOR_DATA = "non_trivial_indicator_data"
TRIVIAL_NETWORK_INDICATOR_DATA = "trivial_network_indicator_data"
NON_TRIVAL_NETWORK_INDICATOR_DATA = "non_trivial_network_indicator_data"

IndicatorDataClassType = t.Literal[
    "trivial_indicator_data",
    "non_trivial_indicator_data",
    "trivial_network_indicator_data",
    "non_trivial_network_indicator_data",
]
TrivialDataType = t.Union[
    int,
    float,
    str,
    bool,
    List[int],
    List[float],
    List[str],
    List["NameAndValue"],
    List["NameNameAndValue"],
]


@dataclass
class TrivialNetworkIndicatorData:
    name: str
    value: "BaseNetworkData[NameAndValue, NameNameAndValue]"
    data_class: t.Literal[
        "trivial_network_indicator_data"
    ] = TRIVIAL_NETWORK_INDICATOR_DATA


@dataclass
class NonTrivalNetworkInciatorData:
    name: str
    value: List[
        "BaseData[BaseNetworkData[ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict]]"
    ]
    data_class: t.Literal[
        "non_trivial_network_indicator_data"
    ] = NON_TRIVAL_NETWORK_INDICATOR_DATA


@dataclass
class TrivialIndicatorData:
    name: str
    value: List["BaseData[TrivialDataType]"]
    data_class: t.Literal["trivial_indicator_data"] = TRIVIAL_INDICATOR_DATA


@dataclass
class NonTrivalIndicatorData:
    name: str
    value: "NonTrivialIndicatorDict"
    data_class: t.Literal[
        "non_trivial_indicator_data"
    ] = NON_TRIVIAL_INDICATOR_DATA


@dataclass
class BaseData(Generic[T]):
    year: int
    month: int
    value: T
    is_raw: bool = False


class NameAndValue(NamedTuple):
    name: str
    value: float

    def __str__(self) -> str:
        return f"\033[34m{self.name}\033[0m: {self.value}"

    def __repr__(self) -> str:
        return f"\033[34m{self.name}\033[0m: {self.value}"


class NameNameAndValue(NamedTuple):
    name0: str
    name1: str
    value: float

    def __str__(self) -> str:
        return f"\033[34m{self.name0}\033[0m>>\033[31m{self.name1}\033[0m: {self.value}"

    def __repr__(self) -> str:
        return f"\033[34m{self.name0}\033[0m>>\033[31m{self.name1}\033[0m: {self.value}"


AvgDataType = BaseData[float]
LevelDataType = BaseData[List[int]]
QuantileDataType = BaseData[float]


class NonTrivialIndicatorDict(TypedDict):
    avg: List[AvgDataType]
    levels: List[LevelDataType]
    quantile0: List[QuantileDataType]
    quantile1: List[QuantileDataType]
    quantile2: List[QuantileDataType]
    quantile3: List[QuantileDataType]
    quantile4: List[QuantileDataType]


class ProjectOpenRankNetworkNodeDict(t.TypedDict):
    id: str
    n: str
    c: str
    i: float
    r: float
    v: float


class ProjectOpenRankNetworkEdgeDict(t.TypedDict):
    s: str
    t: str
    w: float


@dataclass
class BaseNetworkData(Generic[T, S]):
    nodes: List[T]
    edges: List[S]
