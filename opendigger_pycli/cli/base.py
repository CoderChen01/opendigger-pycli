import typing as t

import click

from opendigger_pycli.console.print_base_info import (
    print_repo_info,
    print_user_info,
)
from opendigger_pycli.console import CONSOLE

from .env import Environment
from .custom_types import GH_REPO_NAME_TYPE, GH_USERNAME_TYPE


pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enables verbose mode.",
)
@pass_environment
def opendigger(env: Environment, verbose: bool):
    """Open Digger CLI"""
    env.verbose = verbose


@opendigger.group(invoke_without_command=True)
@click.option(
    "--username",
    "-u",
    "usernames",
    type=GH_USERNAME_TYPE,
    multiple=True,
    help="GitHub username",
)
@pass_environment
def user(env: Environment, usernames: t.List[str]):
    """
    Operate on user metrics
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]requesting users info..."):
            print_user_info(usernames, env.cli_config.github_pat)
    else:
        env.set_mode("user")
        env.set_params(usernames)


@opendigger.group(invoke_without_command=True)
@click.option(
    "--repo",
    "-r",
    "repos",
    type=GH_REPO_NAME_TYPE,
    multiple=True,
    help="GitHub repository, e.g. X-lab2017/open-digger",
    metavar="<org>/<repo>",
)
@pass_environment
def repo(env: Environment, repos: t.List[t.Tuple[str, str]]):
    """
    Operate on repository metrics
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]fetching repos info..."):
            print_repo_info(repos, env.cli_config.github_pat)
    else:
        env.set_mode("repo")
        env.set_params(repos)
