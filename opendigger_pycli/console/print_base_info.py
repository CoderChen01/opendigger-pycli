import typing as t

from rich.table import Table

from opendigger_pycli.utils.git_api import (
    REPO_INFO_DICT,
    get_repo_info,
    get_user_info,
)
from . import CONSOLE


def print_user_info(usernames: t.List[str]):
    pass


def print_repo_info(
    repos: t.List[t.Tuple[str, str]], github_pat: t.Optional[str] = None
):
    table = Table(show_lines=True)
    table.add_column("Repository", overflow="fold")
    table.add_column("Repository URL", overflow="fold")

    name_map = {}
    for key in REPO_INFO_DICT.__annotations__.keys():
        name = " ".join(key.split("_")).title()
        name_map[name] = key
        table.add_column(name, overflow="fold")

    for org_name, repo_name in repos:
        repo_info = get_repo_info(org_name, repo_name, github_pat)
        repo_info = None
        if repo_info is None:
            CONSOLE.print(
                f"[red]fail to request repo [green]{org_name}/{repo_name}[/] [red]info![/]"
            )
            table.add_row(
                f"{org_name}/{repo_name}",
                f"https://www.github.com/{org_name}/{repo_name}",
                *["null" for _ in range(len(name_map))],
            )
        else:
            table.add_row(
                f"{org_name}/{repo_name}",
                f"https://www.github.com/{org_name}/{repo_name}",
                *[str(repo_info[name_map[key]]) for key in name_map],
            )
    CONSOLE.print(table, soft_wrap=True)
