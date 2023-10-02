import typing as t
from dataclasses import dataclass

from .base import (
    BaseData,
    BaseNetworkData,
    NameAndValue,
    NameNameAndValue,
    NonTrivalNetworkInciatorData,
    ProjectOpenRankNetworkEdgeDict,
    ProjectOpenRankNetworkNodeDict,
    TrivialNetworkIndicatorData,
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
    OpenRank’s value orientation:
        Collaborate with high-influencers
        -Developers with high influence bring higher value to issues/PRs,
        and you will be assigned higher values ​​if you have participated in corresponding issues/PRs.
        Generate collaboration -Collaborate with other developers on issues/PRs.
        The more collaboration the issue/PR has, the higher the value,
        and accordingly the value you are assigned will be higher.
        Earn recognition -"likes" gained in issues and PRs,
        "likes" on the main content make the overall value of the issue/PR higher,
        and "likes" on comments make the comment author more valuable
        Contribute more -submit issues and PRs,
        or participate in discussions in issues and PRs Recommended values
    """

    name: t.ClassVar[str] = "project_openrank_detail"
    value: t.List[
        BaseData[
            t.Optional[
                BaseNetworkData[
                    ProjectOpenRankNetworkNodeDict, ProjectOpenRankNetworkEdgeDict
                ]
            ]
        ]
    ]
