import abc
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Optional,
    Generic,
    TypeVar,
    Callable,
    Literal,
)

import requests

from opendigger_pycli.datatypes import (
    BaseData,
    BaseNetworkData,
    ProjectOpenRankNetworkNodeDict,
    ProjectOpenRankNetworkEdgeDict,
    NameAndValue,
    NameNameAndValue,
    NonTrivialMetricDict,
)

DATALOADERS = {}

BASE_API_URL = "https://oss.x-lab.info/open_digger/github/"

T = TypeVar("T")


def get_repo_data(
    org: str, repo: str, metric_name: str, date: Optional[str] = None
) -> Optional[Dict]:
    if date is not None:
        url = f"{BASE_API_URL}{org}/{repo}/{metric_name}/{date}.json"
    else:
        url = f"{BASE_API_URL}{org}/{repo}/{metric_name}.json"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_developer_data(username: str, metric_name: str) -> Optional[Dict]:
    url = f"{BASE_API_URL}{username}/{metric_name}.json"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_base_data(data: Dict[str, Any], load_value: Callable) -> List[BaseData]:
    base_data_list = []

    for date, value in data.items():
        is_raw = False
        if date.endswith("raw"):
            is_raw = True
            date.replace("-raw", "")
        try:
            year, month = date.split("-")[:2]
            year, month = int(year), int(month)
        except Exception:
            # TODO(chenjunjie): add warning
            year, month = (
                0,
                0,
            )  # If the date is not in the correct format, set it to 0

        # value has different types, you need to pass in a function to handle it
        base_data_list.append(
            BaseData(year=year, month=month, is_raw=is_raw, value=load_value(value))
        )

    return base_data_list


def load_name_and_value(data: Tuple[str, float]) -> NameAndValue:
    name, value = data
    return NameAndValue(name=name, value=value)


def load_name_name_and_value(data: Tuple[str, str, float]) -> NameNameAndValue:
    name0, name1, value = data
    return NameNameAndValue(name0=name0, name1=name1, value=value)


def load_avg_data(data: Dict[str, Any]) -> List[BaseData[float]]:
    return load_base_data(data, float)


def load_level_data(data: Dict[str, Any]) -> List[BaseData[List[int]]]:
    return load_base_data(data, lambda x: [int(i) for i in x])


def load_quantile_data(data: Dict[str, Any]) -> List[BaseData[float]]:
    return load_base_data(data, float)


def load_non_trival_metric_data(data: Dict[str, Any]) -> NonTrivialMetricDict:
    return NonTrivialMetricDict(
        avg=load_avg_data(data["avg"]),
        levels=load_level_data(data["levels"]),
        quantile0=load_quantile_data(data["quantile_0"]),
        quantile1=load_quantile_data(data["quantile_1"]),
        quantile2=load_quantile_data(data["quantile_2"]),
        quantile3=load_quantile_data(data["quantile_3"]),
        quantile4=load_quantile_data(data["quantile_4"]),
    )


def load_openrank_network_data(
    data: Dict[str, List],
) -> BaseNetworkData[ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict]:
    nodes = data["nodes"]
    edges = data["links"]
    return BaseNetworkData(nodes=nodes, edges=edges)


def load_network_data(
    data: Dict[str, List]
) -> BaseNetworkData[NameAndValue, NameNameAndValue]:
    nodes = data["nodes"]
    edges = data["edges"]
    return BaseNetworkData(
        nodes=[NameAndValue(name=node[0], value=node[1]) for node in nodes],
        edges=[
            NameNameAndValue(name0=edge[0], name1=edge[1], value=edge[2])
            for edge in edges
        ],
    )


def register_dataloader(cls):
    DATALOADERS[cls.name] = cls
    return cls


@dataclass
class DataloaderState(Generic[T]):
    is_success: bool
    desc: str
    data: Optional[T] = None


class BaseRepoDataloader(abc.ABC, Generic[T]):
    name: str  # Specify the name of the indicator, which is different from the name field in datatypes
    metric_type: Literal[
        "index", "metric", "network"
    ]  # Specifies the type of indicator

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(
        self, org: str, repo: str, date: Optional[str] = None
    ) -> DataloaderState[T]:
        pass


class BaseUserDataloader(abc.ABC, Generic[T]):
    name: str  # Specify the name of the indicator, which is different from the name field in datatypes
    metric_type: Literal["index", "network"]  # Specifies the type of indicator

    @abc.abstractmethod
    def load(self, org: str, repo: str) -> DataloaderState[T]:
        pass
