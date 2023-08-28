import typing as t


from . import CONSOLE
from .termgraph.module import Data, BarChart, Args, Colors
from .termgraph_test import chart

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        BaseNetworkData,
        NameAndValue,
    )


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
            if hasattr(data.value[0], "name"):
                data.value = t.cast(t.List["NameAndValue"], data.value)
                values.append([d.value for d in data.value])
                if data.is_raw:
                    year_months.insert(0, f"{data.year}-{data.month:02}-raw")
                else:
                    year_months.append(f"{data.year}-{data.month:02}")
            continue
        values.append([data.value])

        if data.is_raw:
            year_months.insert(0, f"{data.year}-{data.month:02}-raw")
        else:
            year_months.append(f"{data.year}-{data.month:02}")

    values = [[sum(value)] + value for value in values]

    data = Data(values, year_months, ["value"])

    chart = BarChart(
        data,
        Args(
            colors=[Colors.Red, Colors.Magenta],
            space_between=False,
        ),
    )

    chart.draw()


def print_base_network_data_graph(
    network_data: "BaseNetworkData", *args, **kwargs
):
    pass
