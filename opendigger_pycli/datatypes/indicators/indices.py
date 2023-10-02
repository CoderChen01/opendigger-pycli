from dataclasses import dataclass
from typing import ClassVar, List

from .base import BaseData, NameAndValue, TrivialIndicatorData


@dataclass
class OpenRankData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_2/
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

    name: ClassVar[str] = "openrank"
    value: List[BaseData[float]]


@dataclass
class ActivityData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_1/
    Activity is a statistical indicator proposed by X-lab,
    which weights five collaborative event behaviors:
    issue comment, open issue, open pr, review pr, and pr merged.
    """

    name: ClassVar[str] = "activity"
    value: List[BaseData[float]]


@dataclass
class AttentionData(TrivialIndicatorData):
    """
    ref: https://github.com/X-lab2017/open-digger/issues/1186
    Activity is a statistical metric proposed by the X-lab lab,
    weighted to account for both star
    and fork social collaboration behaviors on GitHub.
    """

    name: ClassVar[str] = "attention"
    value: List[BaseData[int]]
