import typing as t

from rich import box
from rich.table import Table

from opendigger_pycli.dataloaders import filter_dataloader
from opendigger_pycli.utils import THREAD_POOL
from opendigger_pycli.utils.gtihub_api import (
    RepoInfoType,
    UserInfoType,
    get_repo_info,
    get_user_info,
)

from . import CONSOLE


def print_user_info(
    usernames: t.List[str], github_pat: t.Optional[str] = None
) -> Table:
    table = Table(box=box.HORIZONTALS)

    name_map = {}
    for key in UserInfoType.__annotations__.keys():
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
        table.add_row(
            *[
                str(user_info[name_map[key]])  # type: ignore
                for key in name_map
                if "url" not in key
            ]
        )
        table.add_row(
            *[
                f"[link={user_info[name_map[key]]}]{user_info[name_map[key]]}[/link]"  # type: ignore
                for key in name_map
                if "url" in key
            ]
        )

    if not table.rows:
        CONSOLE.print("[red i]No users info...[/]")
        return table

    CONSOLE.print(table)
    return table


def print_repo_info(
    repos: t.List[t.Tuple[str, str]], github_pat: t.Optional[str] = None
) -> Table:
    table = Table(box=box.HORIZONTALS)

    name_map = {}
    for key in RepoInfoType.__annotations__.keys():
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
        table.add_row(
            *[
                str(repo_info[name_map[key]])  # type: ignore
                for key in name_map
                if "url" not in key
            ]
        )
        table.add_row(
            *[
                f"[link={repo_info[name_map[key]]}]{repo_info[name_map[key]]}[/link]"  # type: ignore
                for key in name_map
                if "url" in key
            ]
        )

    if not table.rows:
        CONSOLE.print("[red i]No repos info...[/]")
        return table

    CONSOLE.print(table)
    return table


def print_indicator_info(
    mode: t.Literal["user", "repo"],
    indicator_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
) -> Table:
    table = Table(
        title="[green]Current Query Supporting Indicators[/]",
        box=box.HORIZONTALS,
    )
    table.add_column("Type/Name", overflow="fold")
    table.add_column("Introducer", overflow="fold")
    table.add_column("Demo URL", overflow="fold")

    indicator_dataloaders = filter_dataloader({mode}, indicator_types, introducers)
    for indicator_dataloader in indicator_dataloaders:
        table.add_row(
            f"{indicator_dataloader.indicator_type}/{indicator_dataloader.name}",
            indicator_dataloader.introducer,
            f"[link={indicator_dataloader.demo_url}]{indicator_dataloader.demo_url}[/link]",
        )

    if table.rows:
        CONSOLE.print(table)
        return table

    CONSOLE.print("[red i]No filtered indicators...[/]")
    return table
