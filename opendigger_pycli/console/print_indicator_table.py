import typing as t

from rich import box
from rich.pretty import pretty_repr
from rich.table import Table

from . import CONSOLE
from .utils import if_prettey

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import BaseData, BaseNetworkData


def print_table(table: "Table"):
    if table.rows:
        CONSOLE.print(table)
    else:
        CONSOLE.print("[red]No Data...")
    CONSOLE.print()


def print_base_data_table(base_data_list: t.List["BaseData"], *args, **kwargs):
    title = kwargs.pop("title", None)
    caption = kwargs.pop("caption", None)

    table = Table(
        box=box.HORIZONTALS,
        title_justify="center",
        caption=caption,
        caption_justify="center",
        title=title,
    )
    table.add_column("year", overflow="fold")
    table.add_column("month", overflow="fold")
    table.add_column("value", overflow="fold")

    for data in base_data_list:
        value = (
            str(data.value) if not if_prettey(data.value) else pretty_repr(data.value)
        )

        year = str(data.year) if not data.is_raw else f"[green]{data.year}"
        month = str(data.month) if not data.is_raw else f"[green]{data.month}"
        table.add_row(year, month, value)

    print_table(table)


def print_base_network_data_table(network_data: "BaseNetworkData", *args, **kwargss):
    title = kwargss.pop("title", None)
    caption = kwargss.pop("caption", None)
    table = Table(
        box=box.HORIZONTALS,
        title=title,
        title_justify="center",
        caption=caption,
        caption_justify="center",
    )
    table.add_column("nodes", overflow="fold")
    table.add_column("edges", overflow="fold")
    table.add_row(
        pretty_repr(network_data.nodes, indent_size=2),
        pretty_repr(network_data.edges, indent_size=2),
    )
    print_table(table)
    CONSOLE.print()
