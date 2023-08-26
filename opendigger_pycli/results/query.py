import datetime
import typing as t
from dataclasses import dataclass, field

from rich.progress import track


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import IndicatorQuery, DataloaderProto


@t.overload
def run_dataloader(result: "RepoQueryResult") -> None:
    ...


@t.overload
def run_dataloader(result: "UserQueryResult") -> None:
    ...


def run_dataloader(result) -> None:
    if not isinstance(result, RepoQueryResult) and not isinstance(
        result, UserQueryResult
    ):
        raise TypeError("result must be RepoQueryResult or UserQueryResult")

    process_desc = (
        f"Fetching data for {result.type} {result.username}"
        if isinstance(result, UserQueryResult)
        else f"Fetching data for {result.type} {result.org_name}/{result.repo_name}"
    )
    for dataloader in track(result.dataloaders, description=process_desc):
        if not dataloader.pass_date:
            result.data[dataloader.name] = (
                dataloader.load(
                    result.org_name,
                    result.repo_name,
                )
                if isinstance(result, RepoQueryResult)
                else dataloader.load(result.username)
            )
            continue
        current_indicator_queries = [
            indicator_query[1]
            for indicator_query in result.indicator_queries
            if indicator_query[0] == dataloader.name
            and indicator_query[1] is not None
        ]
        # For indicators that do not specify a query and need to pass in a date query, ignore it directly
        if not current_indicator_queries:
            continue

        current_year = datetime.date.today().year
        dates = set()
        for query in current_indicator_queries:
            for month in query.months:
                dates.add((current_year, month))
            for year in query.years:
                for month in range(1, 13):
                    dates.add((year, month))
            for year_month in query.year_months:
                dates.add(year_month)

        result.data[dataloader.name] = (
            dataloader.load(result.org_name, result.repo_name, list(dates))
            if isinstance(result, "RepoQueryResult")
            else dataloader.load(result.username, list(dates))
        )


@dataclass
class BaseQueryResult:
    type: t.ClassVar[t.Literal["user", "repo"]]
    dataloaders: t.List["DataloaderProto"]
    data: t.Dict[str, t.Any] = field(default_factory=dict, init=False)


@dataclass
class RepoQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["repo"]] = "repo"
    repo: t.Tuple[str, str]
    org_name: str = field(init=False)
    repo_name: str = field(init=False)
    indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]

    def __post_init__(self) -> None:
        self.org_name, self.repo_name = self.repo
        run_dataloader(self)


@dataclass
class UserQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["user"]] = "user"
    username: str
    indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]

    def __post_init__(self) -> None:
        run_dataloader(self)


QueryResults = t.Union[t.List["RepoQueryResult"], t.List["UserQueryResult"]]
