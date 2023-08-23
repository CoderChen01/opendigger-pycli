import typing as t

import click
from click import Parameter, Context

from opendigger_pycli.utils.checkers import exist_gh_repo


class RepoNameType(click.ParamType):
    name = "repo_name"

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


REPO_NAME_TYPE = RepoNameType()
