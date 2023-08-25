import typing as t
from dataclasses import dataclass

from opendigger_pycli.datatypes import BaseRepoResult, BaseUserResult


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import MetricQuery


@dataclass
class QueryRepoResult(BaseRepoResult):
    metric_queries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]]


@dataclass
class QueryUserResult(BaseUserResult):
    metric_queries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]]
