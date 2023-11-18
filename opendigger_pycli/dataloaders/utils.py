import typing as t

import requests

from opendigger_pycli.datatypes import (
    BaseData,
    BaseNetworkData,
    NameAndValue,
    NameNameAndValue,
    ProjectOpenRankNetworkEdgeDict,
    ProjectOpenRankNetworkNodeDict,
    TimeDurationRelatedIndicatorDict,
)

BASE_API_URL = "https://oss.x-lab.info/open_digger/github/"

T = t.TypeVar("T")


def get_repo_data(
    org: str,
    repo: str,
    indicator_name: str,
    date: t.Optional[t.Tuple[int, int]] = None,
) -> t.Optional[t.Dict]:
    if date is not None:
        year, month = date
        url = f"{BASE_API_URL}{org}/{repo}/{indicator_name}/{year}-{month:02}.json"
    else:
        url = f"{BASE_API_URL}{org}/{repo}/{indicator_name}.json"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_developer_data(username: str, indicator_name: str) -> t.Optional[t.Dict]:
    url = f"{BASE_API_URL}{username}/{indicator_name}.json"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_base_data(
    data: t.Dict[str, t.Any], load_value: t.Callable
) -> t.List[BaseData]:
    base_data_list: t.List[BaseData] = []

    for date, value in data.items():
        is_raw = False
        if date.endswith("raw"):
            is_raw = True
            date.replace("-raw", "")
        try:
            year, month = date.split("-")[:2]
        except Exception:
            # TODO(chenjunjie): add warning
            continue

        # value has different types,
        # you need to pass in a function to handle it
        base_data_list.append(
            BaseData(
                year=int(year),
                month=int(month),
                is_raw=is_raw,
                value=load_value(value),
            )
        )

    base_data_list.sort()

    return base_data_list


def load_name_and_value(data: t.Tuple[str, float]) -> NameAndValue:
    name, value = data
    return NameAndValue(name=name, value=value)


def load_name_name_and_value(data: t.Tuple[str, str, float]) -> NameNameAndValue:
    name0, name1, value = data
    return NameNameAndValue(name0=name0, name1=name1, value=value)


def load_avg_data(data: t.Dict[str, t.Any]) -> t.List[BaseData[float]]:
    return load_base_data(data, float)


def load_level_data(data: t.Dict[str, t.Any]) -> t.List[BaseData[t.List[int]]]:
    return load_base_data(data, lambda x: [int(i) for i in x])


def load_quantile_data(data: t.Dict[str, t.Any]) -> t.List[BaseData[float]]:
    return load_base_data(data, float)


def load_non_trival_indicator_data(
    data: t.Dict[str, t.Any]
) -> TimeDurationRelatedIndicatorDict:
    return TimeDurationRelatedIndicatorDict(
        avg=load_avg_data(data["avg"]),
        levels=load_level_data(data["levels"]),
        quantile0=load_quantile_data(data["quantile_0"]),
        quantile1=load_quantile_data(data["quantile_1"]),
        quantile2=load_quantile_data(data["quantile_2"]),
        quantile3=load_quantile_data(data["quantile_3"]),
        quantile4=load_quantile_data(data["quantile_4"]),
    )


def load_openrank_network_data(
    data: t.Dict[str, t.List],
) -> BaseNetworkData[ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict]:
    nodes = data["nodes"]
    edges = data["links"]
    return BaseNetworkData(nodes=nodes, edges=edges)


def load_network_data(
    data: t.Dict[str, t.List]
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
