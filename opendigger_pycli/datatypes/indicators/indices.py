from dataclasses import dataclass
from typing import ClassVar, List

from .base import BaseData, NameAndValue, TrivialIndicatorData


@dataclass
class OpenRankData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_2/
    """

    name: ClassVar[str] = "openrank"
    value: List[BaseData[float]]


@dataclass
class ActivityData(TrivialIndicatorData):
    """
    ref: https://blog.frankzhao.cn/how_to_measure_open_source_1/
    """

    name: ClassVar[str] = "activity_details"
    value: List[BaseData[List[NameAndValue]]]


@dataclass
class AttentionData(TrivialIndicatorData):
    """
    ref: https://github.com/X-lab2017/open-digger/issues/1186
    """

    name: ClassVar[str] = "attention"
    value: List[BaseData[int]]