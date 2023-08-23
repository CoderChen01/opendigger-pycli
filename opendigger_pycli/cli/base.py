import typing as t

import click

from opendigger_pycli.console.print_base_info import (
    print_repo_info,
    print_user_info,
)
from .custom_types import REPO_NAME_TYPE


class OpenDiggerCliConfig:
    def __init__(self):
        self.debug = False
        self.github_pat = "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"

    def set_debug(self, debug: bool):
        self.debug = debug


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
    multiple=True,
    help="GitHub username",
)
@pass_config
def user(config: OpenDiggerCliConfig, usernames: t.List[str]):
    """
    Operate on user metrics
    """
    if click.get_current_context().invoked_subcommand is None:
        print_user_info(usernames)


@opendigger.group(chain=True, invoke_without_command=True)
@click.option(
    "--repo",
    "-r",
    "repos",
    type=REPO_NAME_TYPE,
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
        print_repo_info(repos, config.github_pat)
