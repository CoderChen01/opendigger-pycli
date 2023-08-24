import typing as t

import click
from click import Parameter, Context
from click.core import Context, Parameter
from click.shell_completion import CompletionItem

from opendigger_pycli.utils.checkers import exist_gh_repo, exist_gh_user
from opendigger_pycli.dataloader import DATALOADERS


class GhRepoNameType(click.ParamType):
    name: str = "gh_repo_name"

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
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
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> str:
        if not exist_gh_user(value):
            self.fail(
                f"{value} user does not exist, please check https://www.github.com/{value}"
            )
        return value


class IndexNameType(click.ParamType):
    name: str = "index_name"
    user_indices: t.Dict = {
        name: cls_
        for name, cls_ in DATALOADERS["index"].items()
        if cls_.type == "repo"
    }
    repo_indices: t.Dict = {
        name: cls_
        for name, cls_ in DATALOADERS["index"].items()
        if cls_.type == "repo"
    }
    has_user_metric: bool = True

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> str:
        return value

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> t.List[CompletionItem]:
        return []


class MetricNameType(click.ParamType):
    name: str = "metric_name"
    repo_indices: t.Dict = DATALOADERS["metric"]
    has_user_metric: bool = False

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> str:
        return value

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> t.List[CompletionItem]:
        return []


class NetworkNameType(click.ParamType):
    name: str = "metric_name"
    repo_indices: t.Dict = DATALOADERS["metric"]
    has_user_metric: bool = False

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> str:
        return value

    def shell_complete(
        self, ctx: Context, param: Parameter, incomplete: str
    ) -> t.List[CompletionItem]:
        return []


class AllMetricsType(click.ParamType):
    name: str = "all_metric_names"
    all_metrics = {}

    def __init__(self) -> None:
        super().__init__()
        self.all_metrics = {}
        self.all_metrics.update(DATALOADERS["index"])
        self.all_metrics.update(DATALOADERS["metric"])
        self.all_metrics.update(DATALOADERS["network"])

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> str:
        return value


GH_REPO_NAME_TYPE = GhRepoNameType()
GH_USERNAME_TYPE = GhUserNameType()

INDEX_NAME_TYPE = IndexNameType()
METRIC_NAME_TYPE = MetricNameType()
NETWORK_NAME_TYPE = NetworkNameType()
ALL_METRIC_NAMES_TYPE = AllMetricsType()
