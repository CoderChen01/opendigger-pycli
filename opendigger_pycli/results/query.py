import datetime
import typing as t
from dataclasses import dataclass

from rich.progress import track

from opendigger_pycli.datatypes import BaseRepoResult, BaseUserResult


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import MetricQuery


@t.overload
def run_dataloader(result: "QueryRepoResult") -> None:
    ...


@t.overload
def run_dataloader(result: "QueryUserResult") -> None:
    ...


def run_dataloader(result) -> None:
    if not isinstance(result, QueryRepoResult) and not isinstance(
        result, QueryUserResult
    ):
        raise TypeError("result must be QueryRepoResult or QueryUserResult")

    for dataloader in track(
        result.dataloaders, description="Fecthing data..."
    ):
        if not dataloader.pass_date:
            result.data[dataloader.name] = (
                dataloader.load(
                    result.org_name,
                    result.repo_name,
                )
                if isinstance(result, QueryRepoResult)
                else dataloader.load(result.username)
            )
            continue
        current_metric_queries = [
            metric_query[1]
            for metric_query in result.metric_queries
            if metric_query[0] == dataloader.name
            and metric_query[1] is not None
        ]
        # For indicators that do not specify a query and need to pass in a date query, ignore it directly
        if not current_metric_queries:
            continue

        current_year = datetime.date.today().year
        dates = set()
        for query in current_metric_queries:
            for month in query.months:
                dates.add((current_year, month))
            for year in query.years:
                for month in range(1, 13):
                    dates.add((year, month))
            for year_month in query.year_months:
                dates.add(year_month)

        result.data[dataloader.name] = (
            dataloader.load(result.org_name, result.repo_name, list(dates))
            if isinstance(result, "QueryRepoResult")
            else dataloader.load(result.username, list(dates))
        )


@dataclass
class QueryRepoResult(BaseRepoResult):
    metric_queries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]]

    def __post_init__(self) -> None:
        super().__post_init__()
        run_dataloader(self)


@dataclass
class QueryUserResult(BaseUserResult):
    metric_queries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]]

    def __post_init__(self) -> None:
        super().__post_init__()
        run_dataloader(self)
