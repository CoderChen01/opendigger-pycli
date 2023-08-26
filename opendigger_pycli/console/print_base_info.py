import typing as t

from rich.table import Table
from rich import box

from opendigger_pycli.utils.gtihub_api import (
    REPO_INFO_DICT,
    USER_INFO_DICT,
    get_repo_info,
    get_user_info,
)
from opendigger_pycli.dataloader import filter_dataloader
from opendigger_pycli.utils import THREAD_POOL
from . import CONSOLE


def print_user_info(
    usernames: t.List[str], github_pat: t.Optional[str] = None
):
    table = Table(box=box.HORIZONTALS)

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
        table.add_row(
            *[
                str(user_info[name_map[key]])
                for key in name_map
                if "url" not in key
            ]
        )
        table.add_row(
            *[
                f"[link={user_info[name_map[key]]}]{user_info[name_map[key]]}[/link]"
                for key in name_map
                if "url" in key
            ]
        )
    CONSOLE.print(table)


def print_repo_info(
    repos: t.List[t.Tuple[str, str]], github_pat: t.Optional[str] = None
):
    table = Table(box=box.HORIZONTALS)

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
        table.add_row(
            *[
                str(repo_info[name_map[key]])
                for key in name_map
                if "url" not in key
            ]
        )
        table.add_row(
            *[
                f"[link={repo_info[name_map[key]]}]{repo_info[name_map[key]]}[/link]"
                for key in name_map
                if "url" in key
            ]
        )

    CONSOLE.print(table)


def print_metric_info(
    mode: t.Literal["user", "repo"],
    metric_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
):
    table = Table(
        title="[green]Current Query Supporting Indicators[/]",
        box=box.HORIZONTALS,
    )
    table.add_column("Type/Name", overflow="fold")
    table.add_column("Introducer", overflow="fold")
    table.add_column("Demo URL", overflow="fold")

    metric_dataloaders = filter_dataloader({mode}, metric_types, introducers)
    for metric_dataloader in metric_dataloaders:
        table.add_row(
            f"{metric_dataloader.metric_type}/{metric_dataloader.name}",
            metric_dataloader.introducer,
            f"[link={metric_dataloader.demo_url}]{metric_dataloader.demo_url}[/link]",
        )

    if table.rows:
        CONSOLE.print(table)
    else:
        CONSOLE.print("[red i]No filtered indicators...[/]")
