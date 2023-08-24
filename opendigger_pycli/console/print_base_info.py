import typing as t

from rich.table import Table

from opendigger_pycli.utils.gtihub_api import (
    REPO_INFO_DICT,
    USER_INFO_DICT,
    get_repo_info,
    get_user_info,
)
from opendigger_pycli.utils import THREAD_POOL
from . import CONSOLE


def print_user_info(
    usernames: t.List[str], github_pat: t.Optional[str] = None
):
    with CONSOLE.status("[bold green]requesting users info..."):
        table = Table(show_lines=True)

        name_map = {}
        for key in USER_INFO_DICT.__annotations__.keys():
            name = " ".join(key.split("_")).title()
            name_map[name] = key
            table.add_column(name, overflow="fold")

        results = THREAD_POOL.map(
            lambda username: get_user_info(username, github_pat),
            usernames,
        )

        for is_success, user_info in results:
            if not is_success:
                CONSOLE.print(
                    f"[red]fail to request user [green]{user_info['username']}[/] [red]info![/]"
                )
            table.add_row(*[str(user_info[name_map[key]]) for key in name_map])

        CONSOLE.print(table)


def print_repo_info(
    repos: t.List[t.Tuple[str, str]], github_pat: t.Optional[str] = None
):
    with CONSOLE.status("[bold green]fetching repos info..."):
        table = Table(show_lines=True)

        name_map = {}
        for key in REPO_INFO_DICT.__annotations__.keys():
            name = " ".join(key.split("_")).title()
            name_map[name] = key
            table.add_column(name, overflow="fold")

        results = THREAD_POOL.map(
            lambda repo: get_repo_info(repo[0], repo[1], github_pat),
            repos,
        )

        for is_success, repo_info in results:
            if not is_success:
                CONSOLE.print(
                    f"[red]fail to request repo [green]{repo_info['repository']}[/] [red]info![/]"
                )
            table.add_row(*[str(repo_info[name_map[key]]) for key in name_map])

        CONSOLE.print(table)
