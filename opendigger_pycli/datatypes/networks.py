import typing as t
from dataclasses import dataclass


from .base import (
    BaseData,
    BaseNetworkData,
    NameAndValue,
    NameNameAndValue,
    ProjectOpenRankNetworkEdgeDict,
    ProjectOpenRankNetworkNodeDict,
    TrivialNetworkIndicatorData,
    NonTrivalNetworkInciatorData,
)


@dataclass
class DeveloperNetworkData(TrivialNetworkIndicatorData):
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: t.ClassVar[str] = "developer_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


@dataclass
class RepoNetworkData(TrivialNetworkIndicatorData):
    """
    ref: https://blog.frankzhao.cn/github_activity_with_wpr/
    """

    name: t.ClassVar[str] = "repo_network"
    value: BaseNetworkData[NameAndValue, NameNameAndValue]


@dataclass
class ProjectOpenRankNetworkData(NonTrivalNetworkInciatorData):
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
