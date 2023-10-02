from __future__ import annotations
import copy
import datetime
import typing as t
from dataclasses import dataclass, field, replace

from rich.progress import track

from opendigger_pycli.datatypes import (
    NON_TRIVAL_NETWORK_INDICATOR_DATA,
    NON_TRIVIAL_INDICATOR_DATA,
    TRIVIAL_INDICATOR_DATA,
    TRIVIAL_NETWORK_INDICATOR_DATA,
    IndicatorQuery,
)
from opendigger_pycli.console import CONSOLE
from opendigger_pycli.utils.gtihub_api import (
    create_issue,
    search_issue_title,
    create_issue_comment,
    get_issue_comments,
    create_issue_comment_reactions,
)
from opendigger_pycli.config.utils import get_github_pat, has_github_pat, get_user_info
from opendigger_pycli.utils import THREAD_POOL

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        DataloaderProto,
        DataloaderResult,
        NonTrivalNetworkInciatorData,
        NonTrivialIndicatorData,
        TrivialIndicatorData,
        TrivialNetworkIndicatorData,
    )
    from opendigger_pycli.utils.gtihub_api import IssueCommentInfoType, IssueInfoType


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
        f"Fetching data for {result.type}: [green]{result.username}"
        if isinstance(result, UserQueryResult)
        else f"Fetching data for {result.type}: [green]{result.org_name}/{result.repo_name}"
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
            if indicator_query[0] == dataloader.name and indicator_query[1] is not None
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
            if isinstance(result, RepoQueryResult)
            else dataloader.load(result.username, list(dates))
        )


def merge_indicator_queries(
    indicator_queries: t.List["IndicatorQuery"],
) -> "IndicatorQuery":
    need_years_list = [{year for year in query.years} for query in indicator_queries]
    need_years = set.union(*need_years_list) if need_years_list else set()
    need_months_list = [
        {month for month in query.months} for query in indicator_queries
    ]
    need_months = set.union(*need_months_list) if need_months_list else set()
    need_year_months_list = [
        {year_month for year_month in query.year_months} for query in indicator_queries
    ]
    need_year_months = (
        set.union(*need_year_months_list) if need_year_months_list else set()
    )
    return IndicatorQuery(
        years=frozenset(need_years),
        months=frozenset(need_months),
        year_months=frozenset(need_year_months),
    )


def query_base_data(
    base_data_list: t.List["BaseData"],
    indicator_queries: t.List["IndicatorQuery"],
):
    merged_indicator_query = merge_indicator_queries(indicator_queries)
    success_year_query = set()
    success_month_query = set()
    success_year_month_query = set()

    queried_data = []
    for base_data in base_data_list:
        is_add = False
        if base_data.value is None:
            continue
        if base_data.year in merged_indicator_query.years:
            success_year_query.add(base_data.year)
            is_add = True
        if base_data.month in merged_indicator_query.months:
            success_month_query.add(base_data.month)
            is_add = True
        if (
            base_data.year,
            base_data.month,
        ) in merged_indicator_query.year_months:
            success_year_month_query.add((base_data.year, base_data.month))
            is_add = True
        if not indicator_queries:
            is_add = True

        if not is_add:
            continue
        queried_data.append(base_data)

    faild_query = None
    if (
        merged_indicator_query.years - success_year_query
        or merged_indicator_query.months - success_month_query
        or merged_indicator_query.year_months - success_year_month_query
    ):
        faild_query = IndicatorQuery(
            years=merged_indicator_query.years - success_year_query,
            months=merged_indicator_query.months - success_month_query,
            year_months=merged_indicator_query.year_months,
        )

    return queried_data, faild_query


def query_non_trivial_indicator(
    indicator_data: "NonTrivialIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["NonTrivialIndicatorData", t.Dict[str, t.Optional["IndicatorQuery"]]]:
    queried_indicator_data = copy.deepcopy(indicator_data)
    failed_queries = {}
    for key, base_data_list in indicator_data.value.items():
        base_data_list = t.cast(t.List["BaseData"], base_data_list)
        queried_base_data, failed_query = query_base_data(
            base_data_list, indicator_queries
        )
        queried_indicator_data.value[key] = queried_base_data  # type: ignore
        failed_queries[key] = failed_query
    return queried_indicator_data, failed_queries


def query_trival_indicator(
    indicator_data: "TrivialIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["TrivialIndicatorData", t.Optional["IndicatorQuery"]]:
    queried_base_data_list, failed_query = query_base_data(
        indicator_data.value, indicator_queries
    )
    return replace(indicator_data, value=queried_base_data_list), failed_query


def query_non_trivial_network_indciator(
    indicator_data: "NonTrivalNetworkInciatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["NonTrivalNetworkInciatorData", t.Optional["IndicatorQuery"]]:
    queried_base_data_list, failed_query = query_base_data(
        indicator_data.value, indicator_queries
    )
    return replace(indicator_data, value=queried_base_data_list), failed_query


def query_trivial_network_indicator(
    indicator_data: "TrivialNetworkIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["TrivialNetworkIndicatorData", t.Optional["IndicatorQuery"]]:
    return replace(indicator_data), None


class NodataIssueCreator:
    _github_pat: str

    def __init__(self, title: str, nodata_indicator_names: t.List[str]) -> None:
        self.title = title
        self.nodata_indicator_names = nodata_indicator_names

        self._github_pat = get_github_pat()

        self.has_issue, self.issue_infos = search_issue_title(
            "CoderChen01",
            "opendigger-pycli",
            self.title,
            ["nodata", "bot"],
            self._github_pat,
        )

        self.existed_issue_map: t.Dict[int, IssueInfoType] = {}
        self.existed_nodata_infos: t.Dict[int, t.List[IssueCommentInfoType]] = {}

        if self._has_existed_issue:
            for issue_info in self.issue_infos:  # type: ignore
                self.existed_issue_map[issue_info["issue_number"]] = issue_info

    @property
    def _has_existed_issue(self) -> bool:
        return bool(self.has_issue and self.issue_infos)

    def _create_nodata_issue(self) -> bool:
        if self._has_existed_issue:
            for issue_info in self.issue_infos:  # type: ignore
                (
                    _,
                    self.existed_nodata_infos[issue_info["issue_number"]],
                ) = get_issue_comments(
                    issue_api_url=issue_info["issue_api_url"],
                    github_pat=self._github_pat,
                )
            return True

        is_success, issue_info = create_issue(
            "CoderChen01",
            "opendigger-pycli",
            self._github_pat,
            self.title,
            labels=["nodata", "bot"],
            assignees=["CoderChen01"],
        )
        if is_success and issue_info:
            self.existed_issue_map[issue_info["issue_number"]] = issue_info
            self.existed_nodata_infos[issue_info["issue_number"]] = []
            return True
        return False

    def _add_nodata_info(self) -> None:
        for indicator_name in self.nodata_indicator_names:
            is_ok = False
            for _, issue_comment_infos in self.existed_nodata_infos.items():
                for issue_comment_info in issue_comment_infos:
                    if indicator_name not in issue_comment_info["body"]:
                        continue
                    create_issue_comment_reactions(
                        issue_cooment_api_url=issue_comment_info[
                            "issue_comment_api_url"
                        ],
                        content="eyes",
                        github_pat=self._github_pat,
                    )
                    is_ok = True
                    break
                if is_ok:
                    break
            if is_ok:
                continue
            create_issue_comment(
                issue_api_url=list(self.existed_issue_map.values())[0]["issue_api_url"],
                body=f"No Indicator Data: {indicator_name}",
                github_pat=self._github_pat,
            )

    def run(self) -> None:
        try:
            if not self._create_nodata_issue():
                return
            self._add_nodata_info()
        except Exception:
            return


def run_query(query_result: "BaseQueryResult") -> None:
    indicator_queries = query_result.indicator_queries
    indicators_data = query_result.data

    nodata_indicator_names = []
    for (
        indicator_name,
        indicator_dataloder_result,
    ) in indicators_data.items():
        query_result.failed_query[indicator_name] = None
        current_indicator_queries = (
            [
                indicator_query[1]
                for indicator_query in indicator_queries
                if indicator_query[0] == indicator_name
                and indicator_query[1] is not None
            ]
            if query_result.uniform_query is None
            else [query_result.uniform_query]
        )
        if (
            not indicator_dataloder_result.is_success
            or not indicator_dataloder_result.data
        ):
            nodata_indicator_names.append(indicator_name)
            continue

        indicator_data_class = indicator_dataloder_result.data.data_class
        queried_indciator_data: t.Any
        if indicator_data_class == TRIVIAL_NETWORK_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_trivial_network_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == NON_TRIVAL_NETWORK_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_non_trivial_network_indciator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == TRIVIAL_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_trival_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == NON_TRIVIAL_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_queries,
            ) = query_non_trivial_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
            failed_query_dict = {}
            for key, failed_query in failed_queries.items():
                failed_query_dict[key] = failed_query
            query_result.failed_query[indicator_name] = failed_query_dict
            query_result.queried_data[indicator_name] = replace(
                indicator_dataloder_result, data=queried_indciator_data
            )
            continue
        else:
            raise ValueError(
                f"Unknown indicator data class: {indicator_dataloder_result}"
            )
        query_result.failed_query[indicator_name] = failed_query
        query_result.queried_data[indicator_name] = replace(
            indicator_dataloder_result, data=queried_indciator_data
        )

    if not nodata_indicator_names:
        return

    if query_result.type == "user":
        query_result = t.cast("UserQueryResult", query_result)
        title = f"User: {query_result.username}"
        print_str = f"{title}, Indicator Names: {str(nodata_indicator_names)}, No Data"
    else:
        query_result = t.cast("RepoQueryResult", query_result)
        title = f"Repo: {query_result.org_name}/{query_result.repo_name}"
        print_str = f"{title}, Indicator Names: {str(nodata_indicator_names)}, No Data"

    CONSOLE.print(f"[red]{print_str}[/red]")
    if not has_github_pat():
        CONSOLE.print(
            "[yellow]You can config github personal access token to create issues automatically[/yellow]"
        )
        return
    with CONSOLE.status("Issues being returned to OpenDigger..."):
        NodataIssueCreator(title, nodata_indicator_names).run()


@dataclass
class BaseQueryResult:
    type: t.ClassVar[t.Literal["user", "repo"]]
    dataloaders: t.List["DataloaderProto"]
    indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]
    uniform_query: t.Optional["IndicatorQuery"]
    data: t.Dict[str, "DataloaderResult"] = field(default_factory=dict, init=False)
    queried_data: t.Dict[str, "DataloaderResult"] = field(
        default_factory=dict, init=False
    )
    failed_query: t.Dict[
        str,
        t.Union[
            t.Optional["IndicatorQuery"],
            t.Dict[str, t.Optional["IndicatorQuery"]],
        ],
    ] = field(default_factory=dict, init=False)


@dataclass
class RepoQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["repo"]] = "repo"
    repo: t.Tuple[str, str]
    org_name: str = field(init=False)
    repo_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.org_name, self.repo_name = self.repo
        run_dataloader(self)
        run_query(self)


@dataclass
class UserQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["user"]] = "user"
    username: str

    def __post_init__(self) -> None:
        run_dataloader(self)
        run_query(self)


QueryResults = t.Union[t.List["RepoQueryResult"], t.List["UserQueryResult"]]
