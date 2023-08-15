from dataclasses import dataclass
from typing import TypedDict, ClassVar


from .base import BaseData, BaseNetworkData, NameAndValue, NameNameAndValue


@dataclass
class DeveloperNetworkData:
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: ClassVar[str] = "developer_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


@dataclass
class RepoNetworkData:
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: ClassVar[str] = "repo_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


class ProjectOpenRankNetworkNodeDict(TypedDict):
    id: str
    n: str
    c: str
    i: float
    r: float
    v: float


class ProjectOpenRankNetworkEdgeDict(TypedDict):
    s: str
    t: str
    w: float


@dataclass
class ProjectOpenRankNetworkData:
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_3/
    """

    name: ClassVar[str] = "project_openrank_detail"
    value: BaseData[
        BaseNetworkData[ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict]
    ]
