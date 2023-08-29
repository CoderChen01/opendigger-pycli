import typing as t
from dataclasses import dataclass
from typing import Generic, List, NamedTuple, TypedDict, TypeVar

T = TypeVar("T")
S = TypeVar("S")

TRIVIAL_INDICATOR_DATA: t.Literal["trivial_indicator_data"] = "trivial_indicator_data"
NON_TRIVIAL_INDICATOR_DATA: t.Literal[
    "non_trivial_indicator_data"
] = "non_trivial_indicator_data"
TRIVIAL_NETWORK_INDICATOR_DATA: t.Literal[
    "trivial_network_indicator_data"
] = "trivial_network_indicator_data"
NON_TRIVAL_NETWORK_INDICATOR_DATA: t.Literal[
    "non_trivial_network_indicator_data"
] = "non_trivial_network_indicator_data"

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
    name: t.ClassVar[str]
    value: "BaseNetworkData[NameAndValue, NameNameAndValue]"
    data_class: t.Literal[
        "trivial_network_indicator_data"
    ] = TRIVIAL_NETWORK_INDICATOR_DATA


@dataclass
class NonTrivalNetworkInciatorData:
    name: t.ClassVar[str]
    value: List[
        "BaseData[t.Optional[BaseNetworkData[ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict]]]"
    ]
    data_class: t.Literal[
        "non_trivial_network_indicator_data"
    ] = NON_TRIVAL_NETWORK_INDICATOR_DATA


@dataclass
class TrivialIndicatorData:
    name: t.ClassVar[str]
    value: List["BaseData[TrivialDataType]"]
    data_class: t.Literal["trivial_indicator_data"] = TRIVIAL_INDICATOR_DATA


@dataclass
class NonTrivialIndicatorData:
    name: t.ClassVar[str]
    value: "NonTrivialIndicatorDict"
    data_class: t.Literal["non_trivial_indicator_data"] = NON_TRIVIAL_INDICATOR_DATA


class BaseDataValueSortableMixin:
    def __post_init__(self):
        if not isinstance(self.value, list):
            return
        warmup = self.value[0]
        if isinstance(warmup, int) or isinstance(warmup, float):
            self.value = list(sorted(self.value, reverse=True))  # type: ignore
        if hasattr(warmup, "value"):
            self.value = list(sorted(self.value, key=lambda x: x.value, reverse=True))  # type: ignore
        if isinstance(warmup, dict) and "value" in warmup:
            self.value = list(sorted(self.value, key=lambda x: x["value"], reverse=True))  # type: ignore


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

    def __post_init__(self):
        if isinstance(self.nodes[0], NameAndValue):
            self.nodes = list(sorted(self.nodes, key=lambda x: x.value, reverse=True))  # type: ignore
            self.edges = list(sorted(self.edges, key=lambda x: x.value, reverse=True))  # type: ignore
