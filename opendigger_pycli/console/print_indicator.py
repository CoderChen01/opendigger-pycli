import typing as t

from opendigger_pycli.datatypes.query import IndicatorQuery

from . import CONSOLE
from .print_indicator_graph import print_base_data_graph, print_base_network_data_graph
from .print_indicator_json import (
    print_base_data_json,
    print_base_network_data_json,
    print_time_duration_related_indicator_json,
)
from .print_indicator_table import print_base_data_table, print_base_network_data_table
from .utils import print_failed_query

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        NonTrivalNetworkInciatorData,
        NonTrivialIndicatorData,
        TrivialIndicatorData,
        TrivialNetworkIndicatorData,
    )

SURPPORTED_DISPLAY_FORMATS = ["table", "graph", "json"]
SURPPORTED_DISPLAY_FORMAT_TYPE = t.Literal["table", "graph", "json"]


def format_indicator_name(indicator_name: str) -> str:
    return indicator_name.replace("_", " ").title()


def print_trivial_indicator(
    indicator_name: str,
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
    indicator_name = format_indicator_name(indicator_name)
    title = f"[green]{indicator_name} Indicator Data: "
    CONSOLE.print(title, end="\n\n")
    print_failed_query(indicator_name, failed_query)
    print_func(indicator_data.value)


def print_non_trivial_indicator(
    indicator_name: str,
    indicator_data: "NonTrivialIndicatorData",
    failed_queries: t.Dict[str, "IndicatorQuery"],
    mode: t.Literal["table", "json", "graph"],
):
    print_func: t.Optional[t.Callable] = None

    if mode == "table":
        print_func = print_base_data_table
    elif mode == "graph":
        print_func = print_base_data_graph

    indicator_name_formated = format_indicator_name(indicator_name)
    title = f"[green]{indicator_name_formated} Indicator Data: "
    CONSOLE.print(title, end="\n\n")

    if mode == "json":
        print_time_duration_related_indicator_json(indicator_data.value)
        return

    if print_func is None:
        return
    for key, base_data_list in indicator_data.value.items():
        if failed_queries is not None:
            print_failed_query(f"{indicator_name}.{key}", failed_queries[key])
        base_data_list = t.cast(t.List["BaseData"], base_data_list)
        print_func(base_data_list, caption=f"{indicator_name}.{key}")


def print_trivial_network_indicator(
    indicator_name: str,
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

    indicator_name = format_indicator_name(indicator_name)
    title = f"[green]{indicator_name} Indicator Data: "
    CONSOLE.print(title, end="\n\n")
    print_failed_query(indicator_name, failed_query)
    print_func(indicator_data.value)


def print_non_trivial_network_indciator(
    indicator_name: str,
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

    indicator_name = format_indicator_name(indicator_name)
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
