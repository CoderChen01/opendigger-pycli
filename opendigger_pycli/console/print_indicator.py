import typing as t

from rich.table import Table
from rich.pretty import Pretty
from rich import box


from opendigger_pycli.console import CONSOLE
from opendigger_pycli.datatypes.query import IndicatorQuery

from .termgraph.module import Data, BarChart, Args, Colors
from .termgraph_test import chart

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        TrivialIndicatorData,
        NonTrivialIndicatorData,
        TrivialNetworkIndicatorData,
        NonTrivalNetworkInciatorData,
        BaseData,
        BaseNetworkData,
        NameAndValue,
        NameNameAndValue,
    )

SURPPORTED_DISPLAY_FORMATS = ["table", "graph", "json"]
SURPPORTED_DISPLAY_FORMAT_TYPE = t.Literal["table", "graph", "json"]


def get_indicator_name(indicator_name: str) -> str:
    return indicator_name.replace("_", " ").title()


def if_prettey(value: t.Any) -> bool:
    if isinstance(value, list):
        if hasattr(value[0], "name"):
            value = t.cast(t.List["NameAndValue"], value)
            return True
        if hasattr(value[0], "name0"):
            value = t.cast(t.List["NameNameAndValue"], value)
            return True
    return False


def print_table(table: "Table"):
    if table.rows:
        CONSOLE.print(table)
    else:
        CONSOLE.print("[red]No Data...")
    CONSOLE.print()


def print_base_data_table(base_data_list: t.List["BaseData"], *args, **kwarg):
    title = kwarg.pop("title", None)
    caption = kwarg.pop("caption", None)

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
            str(data.value)
            if not if_prettey(data.value)
            else Pretty(data.value)
        )

        year = str(data.year) if not data.is_raw else f"[green]{data.year}"
        month = str(data.month) if not data.is_raw else f"[green]{data.month}"
        table.add_row(year, month, value)

    print_table(table)


def print_base_data_json(base_data_list: t.List["BaseData"], *args, **kwarg):
    rows_data = []
    for data in base_data_list:
        value = (
            str(data.value)
            if not if_prettey(data.value)
            else Pretty(data.value)
        )

        year = str(data.year) if not data.is_raw else f"[green]{data.year}"
        month = str(data.month) if not data.is_raw else f"[green]{data.month}"
        rows_data.append(
            {
                "year": year,
                "month": month,
                "value": value,
                "is_raw": data.is_raw,
            }
        )
    CONSOLE.print(rows_data)
    CONSOLE.print()


def print_base_data_graph(base_data_list: t.List["BaseData"], *args, **kwargs):
    values = []
    year_months = []
    for data in base_data_list:
        # value = (
        #     str(data.value)
        #     if not if_prettey(data.value)
        #     else Pretty(data.value)
        # )
        if isinstance(data.value, list):
            continue
        values.append([data.value])

        if data.is_raw:
            year_months.insert(0, f"[green]{data.year}-{data.month:02}-raw[/]")
        else:
            year_months.append(f"[black]{data.year}-{data.month:02}[/]")

    data = Data(values, year_months, ["value"])

    chart = BarChart(
        data,
        Args(
            colors=[Colors.Red, Colors.Magenta],
            space_between=False,
        ),
    )

    chart.draw()


def print_base_network_data_table(
    network_data: "BaseNetworkData", *args, **kwargs
):
    title = kwargs.pop("title", None)
    caption = kwargs.pop("caption", None)
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
        Pretty(network_data.nodes, indent_size=2),
        Pretty(network_data.edges, indent_size=2),
    )
    print_table(table)
    CONSOLE.print()


def print_base_network_data_json(
    network_data: "BaseNetworkData", *args, **kwargs
):
    pass


def print_base_network_data_graph(
    network_data: "BaseNetworkData", *args, **kwargs
):
    pass


def print_failed_query(
    indicator_name: str, failed_query: t.Optional["IndicatorQuery"]
) -> None:
    if failed_query is None:
        return

    if failed_query.years:
        CONSOLE.print(
            f"[red]No {indicator_name} Indicator Data in years: "
            f"{list(failed_query.years)}"
        )
    if failed_query.months:
        CONSOLE.print(
            f"[red]No {indicator_name} Indicator Data in months: "
            f"{list(failed_query.months)}"
        )
    if failed_query.year_months:
        CONSOLE.print(
            f"[red]No {indicator_name} Indicator Data in year_months: "
            f"{[f'{year_month[0]}-{year_month[1]:02}' for year_month in failed_query.year_months]}"
        )


def print_trivial_indicator(
    indicator_data: "TrivialIndicatorData",
    failed_query: t.Optional["IndicatorQuery"],
    mode: t.Literal["table", "json", "graph"],
):
    print_func: t.Optional[t.Callable] = None

    if mode == "table":
        print_func = print_base_data_table
    elif mode == "json":
        print_func = print_base_data_json
    elif mode == "graph":
        print_func = print_base_data_graph

    if print_func is None:
        return
    indicator_name = get_indicator_name(indicator_data.name)
    title = f"[green]{indicator_name} Indicator Data: "
    CONSOLE.print(title)
    print_failed_query(indicator_name, failed_query)
    print_func(indicator_data.value)


def print_non_trivial_indicator(
    indicator_data: "NonTrivialIndicatorData",
    failed_queries: t.Dict[str, "IndicatorQuery"],
    mode: t.Literal["table", "json", "graph"],
):
    print_func: t.Optional[t.Callable] = None

    if mode == "table":
        print_func = print_base_data_table
    elif mode == "json":
        print_func = print_base_data_json
    elif mode == "graph":
        print_func = print_base_data_graph

    if print_func is None:
        return

    indicator_name = get_indicator_name(indicator_data.name)
    title = f"[green]{indicator_name} Indicator Data: "
    CONSOLE.print(title)
    for key, base_data_list in indicator_data.value.items():
        if failed_queries is not None:
            print_failed_query(
                f"{indicator_data.name}.{key}", failed_queries[key]
            )
        base_data_list = t.cast(t.List["BaseData"], base_data_list)
        print_func(base_data_list, caption=f"{indicator_data.name}.{key}")


def print_trivial_network_indicator(
    indicator_data: "TrivialNetworkIndicatorData",
    failed_query: t.Optional["IndicatorQuery"],
    mode: t.Literal["table", "json", "graph"],
):
    print_func: t.Optional[t.Callable] = None

    if mode == "table":
        print_func = print_base_network_data_table
    elif mode == "json":
        print_func = print_base_network_data_json
    elif mode == "graph":
        print_func = print_base_network_data_graph

    if print_func is None:
        return

    indicator_name = get_indicator_name(indicator_data.name)
    title = f"[green]{indicator_name} Indicator Data: "
    CONSOLE.print(title)
    print_failed_query(indicator_name, failed_query)
    print_func(indicator_data.value)


def print_non_trivial_network_indciator(
    indicator_data: "NonTrivalNetworkInciatorData",
    failed_query: t.Optional["IndicatorQuery"],
    mode: t.Literal["table", "json", "graph"],
):
    print_func: t.Optional[t.Callable] = None

    if mode == "table":
        print_func = print_base_network_data_table
    elif mode == "json":
        print_func = print_base_network_data_json
    elif mode == "graph":
        print_func = print_base_network_data_graph

    if print_func is None:
        return

    indicator_name = get_indicator_name(indicator_data.name)
    CONSOLE.print(f"[green]{indicator_name} Indicator Data: ")
    print_failed_query(indicator_name, failed_query)
    for data in indicator_data.value:
        if data.value is None:
            CONSOLE.print(
                f"No {indicator_name} Indicator Data at {data.year}-{data.month:02}"
            )
            continue
        print_func(
            data.value,
            caption=f"at {data.year}-{data.month:02}",
        )
