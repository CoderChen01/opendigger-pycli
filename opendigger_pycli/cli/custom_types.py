import typing as t

import click
from click.shell_completion import CompletionItem

from opendigger_pycli.dataloader import (
    DeveloperNetworkRepoDataloader,
    ProjectOpenRankNetworkRepoDataloader,
    RepoNetworkRepoDataloader,
)
from opendigger_pycli.utils.checkers import exist_gh_repo, exist_gh_user

from .parsers import QueryParser

if t.TYPE_CHECKING:
    from click.core import Context, Parameter

    from opendigger_pycli.datatypes import IndicatorQuery


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
                    f"{value} repo does not exist, "
                    f"please check https://www.github.com/{org_name}/{repo_name}"
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
                f"{value} user does not exist, "
                f"please check https://www.github.com/{value}"
            )
        return value


class FilteredMetricQueryType(click.ParamType):
    name: t.ClassVar[str] = "indicator_query"

    def __init__(self) -> None:
        super().__init__()
        self.query_parser = QueryParser()

    def _try_split_value(self, value: str) -> t.Tuple[str, t.Optional[str]]:
        value = value.strip()
        try:
            indicator_name, indicator_query = value.split(":", 1)
            return indicator_name.strip(), indicator_query.strip()
        except ValueError:
            return value, None

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> t.Tuple[str, t.Optional["IndicatorQuery"]]:
        indicator_name, indicator_query_str = self._try_split_value(value)
        if indicator_name not in ctx.meta["filtered_dataloaders"]:
            self.fail(
                f"{indicator_name} is not a valid indicator name "
                f"for filtered indicator info, "
                f"METRIC_TYPES: {ctx.params['indicator_types']}, "
                f"INTRODUCERS: {ctx.params['introducers']}"
            )
        if indicator_query_str is None:
            if (
                indicator_name == ProjectOpenRankNetworkRepoDataloader.name
                and ctx.params["uniform_query"] is None
            ):
                self.fail(
                    f"{indicator_name} requires indicator query, "
                    f"please use {indicator_name}:<indicator-queries>"
                )
            return indicator_name, None
        elif (
            indicator_name == DeveloperNetworkRepoDataloader.name
            or indicator_name == RepoNetworkRepoDataloader.name
        ):
            self.fail(
                f"{indicator_name} does not support indicator query, "
                f"please use {indicator_name} directly"
            )

        indicator_query = self.query_parser.try_parse_indicator_query(
            indicator_query_str
        )
        if indicator_query is None:
            self.fail(f"{indicator_query_str} is not a valid indicator query")

        return indicator_name, indicator_query

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> t.List[CompletionItem]:
        incomplete, query_str = self._try_split_value(incomplete)
        return [
            CompletionItem(name if query_str is None else f"{name}:{query_str}")
            for name in ctx.meta["filtered_dataloaders"]
            if name.startswith(incomplete)
        ]


class IgnoredIndicatorNameType(click.ParamType):
    name: t.ClassVar[str] = "ignored_indicator_names"

    def convert(
        self,
        value: str,
        param: "Parameter",
        ctx: "Context",
    ) -> str:
        indicator_name = value
        if indicator_name not in ctx.meta["filtered_dataloaders"]:
            self.fail(
                f"{indicator_name} is not a valid indicator name "
                f"for filtered indicator info, "
                f"METRIC_TYPES: {ctx.params['indicator_types']}, "
                f"INTRODUCERS: {ctx.params['introducers']}"
            )

        return indicator_name

    def shell_complete(
        self, ctx: "Context", param: "Parameter", incomplete: str
    ) -> t.List[CompletionItem]:
        return [
            CompletionItem(name)
            for name in ctx.meta["filtered_dataloaders"]
            if name.startswith(incomplete)
        ]


class IndicatorQueryType(click.ParamType):
    name = "indicator_query"

    def __init__(self) -> None:
        super().__init__()
        self.query_parser = QueryParser()

    def convert(
        self, value: str, param: "Parameter", ctx: "Context"
    ) -> "IndicatorQuery":
        query = self.query_parser.try_parse_indicator_query(value)
        if query is None:
            self.fail(f"{value} is not a valid indicator query")
        return query


GH_REPO_NAME_TYPE = GhRepoNameType()
GH_USERNAME_TYPE = GhUserNameType()

FILTERED_METRIC_QUERY_TYPE = FilteredMetricQueryType()
IGNORED_METRIC_NAME_TYPE = IgnoredIndicatorNameType()
INDICATOR_QUERY_TYPE = IndicatorQueryType()
