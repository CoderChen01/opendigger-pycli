import typing as t

import click

from opendigger_pycli.console.print_base_info import (
    print_repo_info,
    print_user_info,
)
from .custom_types import REPO_NAME_TYPE


# OpenDiggerCliConfig 类，用于存储配置信息
class OpenDiggerCliConfig:
    def __init__(self):
        self.debug = False
        self.github_pat = "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"

    def set_debug(self, debug: bool):
        self.debug = debug


# 使用 click 的 make_pass_decorator 创建 config 的装饰器
pass_config = click.make_pass_decorator(OpenDiggerCliConfig, ensure=True)


# 创建一个命令组 opendigger
@click.group()
@click.option(
    "--debug/--no-debug", default=False, help="Enable or disable debug mode"
)
@pass_config
def opendigger(config: OpenDiggerCliConfig, debug: bool):
    config.debug = debug


# 在 opendigger 命令组中创建子命令 user
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
    # 如果没有子命令，调用 print_user_info 函数打印用户信息
    if click.get_current_context().invoked_subcommand is None:
        print_user_info(usernames)


# 在 opendigger 命令组中创建子命令 repo
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
    # 如果没有子命令，调用 print_repo_info 函数打印仓库信息，传入 github_pat
    if click.get_current_context().invoked_subcommand is None:
        print_repo_info(repos, config.github_pat)
