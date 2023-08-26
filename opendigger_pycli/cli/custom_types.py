import typing as t

import click
from click.core import Context, Parameter
from click.shell_completion import CompletionItem

from opendigger_pycli.utils.checkers import exist_gh_repo, exist_gh_user
from opendigger_pycli.dataloader import ProjectOpenRankNetworkRepoDataloader
from opendigger_pycli.datatypes import IndicatorQuery


if t.TYPE_CHECKING:
    from click import Context, Parameter, Command
    from opendigger_pycli.datatypes import DataloaderProto


class GhRepoNameType(click.ParamType):
    name: str = "gh_repo_name"

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> t.Tuple[str, str]:
        try:
            org_name, repo_name = value.split("/")
            if not exist_gh_repo(org_name, repo_name):
                self.fail(
                    f"{value} repo does not exist, please check https://www.github.com/{org_name}/{repo_name}"
                )
            return org_name, repo_name
        except ValueError:
            self.fail(f"{value} is not a valid repo name")


class GhUserNameType(click.ParamType):
    name: str = "gh_username"

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> str:
        if not exist_gh_user(value):
            self.fail(
                f"{value} user does not exist, please check https://www.github.com/{value}"
            )
        return value


class FilteredMetricQueryType(click.ParamType):
    name: t.ClassVar[str] = "indicator_query"

    def _try_split_value(self, value: str) -> t.Tuple[str, t.Optional[str]]:
        value = value.strip()
        try:
            indicator_name, indicator_query = value.split(":", 1)
            return indicator_name.strip(), indicator_query.strip()
        except ValueError:
            return value, None

    def _try_parse_month(self, item: str) -> t.Optional[t.Set[int]]:
        if "~" in item:
            try:
                start, end = item.split("~", 1)
                start = int(start)
                end = int(end)
                if start > end:
                    return None
                if start < 1 or end > 12:
                    return None
                return set(range(start, end + 1))
            except ValueError:
                return None
        else:
            try:
                month = int(item)
                if month < 1 or month > 12:
                    return None
                return {month}
            except ValueError:
                return None

    def _try_parse_year(self, item: str) -> t.Optional[t.Set[int]]:
        if "~" in item:
            try:
                start, end = item.split("~", 1)
                start = int(start)
                end = int(end)
                if start > end:
                    return None
                if start < 1970 or end > 2100:
                    return None
                return set(range(start, end + 1))
            except ValueError:
                return None
        else:
            try:
                year = int(item)
                if year < 1970 or year > 2100:
                    return None
                return {year}
            except ValueError:
                return None

    def _try_parse_year_month(
        self, item: str
    ) -> t.Optional[t.Set[t.Tuple[int, int]]]:
        if "~" in item:
            try:
                start, end = item.split("~", 1)
                start_year, start_month = start.split("-", 1)
                end_year, end_month = end.split("-", 1)
                start_year = int(start_year)
                start_month = int(start_month)
                end_year = int(end_year)
                end_month = int(end_month)
                if start_year > end_year:
                    return None
                if start_year < 1970 or end_year > 2100:
                    return None
                if start_month > end_month:
                    return None
                if start_month < 1 or end_month > 12:
                    return None

                result = set()
                current_year = start_year
                current_month = start_month
                while (current_year, current_month) <= (end_year, end_month):
                    result.add((current_year, current_month))
                    current_month += 1
                    if current_month > 12:
                        current_month = 1
                        current_year += 1
                return result

            except ValueError:
                return None
        else:
            try:
                year, month = item.split("-", 1)
                year = int(year)
                month = int(month)
                if year < 1970 or year > 2100:
                    return None
                if month < 1 or month > 12:
                    return None
                return {(year, month)}
            except ValueError:
                return None

    def _try_parse_indicator_query(
        self, indicator_query: str
    ) -> t.Optional[IndicatorQuery]:
        all_months = set()
        all_years = set()
        all_year_months = set()

        indicator_query = indicator_query.strip()
        items = indicator_query.split(",")
        for item in items:
            months = self._try_parse_month(item)
            if months is not None:
                all_months.update(months)
                continue
            years = self._try_parse_year(item)
            if years is not None:
                all_years.update(years)
                continue
            year_months = self._try_parse_year_month(item)
            if year_months is not None:
                all_year_months.update(year_months)
                continue
            if not months and not years and not year_months:
                self.fail(f"{item} is not a valid indicator query")

        if not all_months and not all_years and not all_year_months:
            return None

        return IndicatorQuery(
            months=frozenset(all_months),
            years=frozenset(all_years),
            year_months=frozenset(all_year_months),
        )

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> t.Tuple[str, t.Optional[IndicatorQuery]]:
        indicator_name, indicator_query_str = self._try_split_value(value)
        if (
            indicator_name
            not in ctx.meta[
                f"opendigger_pycli.cli.query_cmd.filtered_dataloaders"
            ]
        ):
            self.fail(
                f"{indicator_name} is not a valid indicator name for filtered indicator info, \
                METRIC_TYPES: {ctx.params['indicator_types']}, \
                INTRODUCERS: {ctx.params['introducers']}"
            )
        if indicator_query_str is None:
            if indicator_name == ProjectOpenRankNetworkRepoDataloader.name:
                self.fail(
                    f"{indicator_name} requires indicator query, \
                    please use {indicator_name}:<indicator-queries>"
                )
            return indicator_name, None

        indicator_query = self._try_parse_indicator_query(indicator_query_str)
        if indicator_query is None:
            self.fail(f"{indicator_query_str} is not a valid indicator query")

        return indicator_name, indicator_query

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> t.List[CompletionItem]:
        incomplete, query_str = self._try_split_value(incomplete)
        return [
            CompletionItem(
                name if query_str is None else f"{name}:{query_str}"
            )
            for name in ctx.meta[
                f"opendigger_pycli.cli.query_cmd.filtered_dataloaders"
            ]
            if name.startswith(incomplete)
        ]


class IgnoredMetricNameType(click.ParamType):
    name: t.ClassVar[str] = "ignored_indicator_names"

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> str:
        indicator_name = value
        if (
            indicator_name
            not in ctx.meta[
                f"opendigger_pycli.cli.query_cmd.filtered_dataloaders"
            ]
        ):
            self.fail(
                f"{indicator_name} is not a valid indicator name for filtered indicator info, \
                METRIC_TYPES: {ctx.params['indicator_types']}, \
                INTRODUCERS: {ctx.params['introducers']}"
            )

        return indicator_name

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> t.List[CompletionItem]:
        return [
            CompletionItem(name)
            for name in ctx.meta[
                f"opendigger_pycli.cli.query_cmd.filtered_dataloaders"
            ]
            if name.startswith(incomplete)
        ]


GH_REPO_NAME_TYPE = GhRepoNameType()
GH_USERNAME_TYPE = GhUserNameType()

FILTERED_METRIC_QUERY_TYPE = FilteredMetricQueryType()
IGNORED_METRIC_NAME_TYPE = IgnoredMetricNameType()
