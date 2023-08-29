from dataclasses import dataclass
from typing import ClassVar

from .base import TrivialIndicatorData


@dataclass
class OpenRankData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_2/
    """

    name: ClassVar[str] = "openrank"


@dataclass
class ActivityData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_1/
    """

    name: ClassVar[str] = "activity_details"


@dataclass
class AttentionData(TrivialIndicatorData):
    """
    ref: https://github.com/X-lab2017/open-digger/issues/1186
    """

    name: ClassVar[str] = "attention"
