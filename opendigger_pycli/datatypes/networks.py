import typing as t
from dataclasses import dataclass


from .base import BaseData, BaseNetworkData, NameAndValue, NameNameAndValue


@dataclass
class DeveloperNetworkData:
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: t.ClassVar[str] = "developer_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


@dataclass
class RepoNetworkData:
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: t.ClassVar[str] = "repo_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


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
class ProjectOpenRankNetworkData:
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_3/
    """

    name: t.ClassVar[str] = "project_openrank_detail"
    value: t.List[
        BaseData[
            BaseNetworkData[
                ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict
            ]
        ]
    ]
