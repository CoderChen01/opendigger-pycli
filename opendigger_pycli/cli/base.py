import typing as t

import click

from opendigger_pycli.console.print_base_info import (
    print_repo_info,
    print_user_info,
)
from opendigger_pycli.config.cli_config import OpenDiggerCliConfig
from opendigger_pycli.console import CONSOLE
from .custom_types import GH_REPO_NAME_TYPE, GH_USERNAME_TYPE


pass_config = click.make_pass_decorator(OpenDiggerCliConfig, ensure=True)


@click.group()
@click.option(
    "--debug/--no-debug", default=False, help="Enable or disable debug mode"
)
@pass_config
def opendigger(config: OpenDiggerCliConfig, debug: bool):
    config.debug = debug


@opendigger.group(chain=True, invoke_without_command=True)
@click.option(
    "--username",
    "-u",
    "usernames",
    type=GH_USERNAME_TYPE,
    multiple=True,
    help="GitHub username",
)
@pass_config
def user(config: OpenDiggerCliConfig, usernames: t.List[str]):
    """
    Operate on user metrics
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]requesting users info..."):
            print_user_info(usernames)


@opendigger.group(chain=True, invoke_without_command=True)
@click.option(
    "--repo",
    "-r",
    "repos",
    type=GH_REPO_NAME_TYPE,
    multiple=True,
    help="GitHub repository, e.g. X-lab2017/open-digger",
    metavar="<org>/<repo>",
)
@pass_config
def repo(config: OpenDiggerCliConfig, repos: t.List[t.Tuple[str, str]]):
    """
    Operate on repository metrics
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]fetching repos info..."):
            print_repo_info(repos, config.github_pat)
