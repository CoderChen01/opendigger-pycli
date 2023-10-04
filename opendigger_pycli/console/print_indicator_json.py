from __future__ import annotations
import typing as t
from dataclasses import asdict

from rich.pretty import Pretty


from . import CONSOLE
from .utils import if_prettey

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        BaseNetworkData,
        TimeDurationRelatedIndicatorDict,
    )


def print_base_data_json(base_data_list: t.List["BaseData"], *args, **kwarg):
    rows_data = []
    for data in base_data_list:
        value = str(data.value) if not if_prettey(data.value) else Pretty(data.value)

        year = str(data.year)
        month = str(data.month)
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


def print_time_duration_related_indicator_json(
    dat: TimeDurationRelatedIndicatorDict, *args, **kwargs
):
    to_print_dict = {}
    for key, value in dat.items():
        to_print_dict[key] = [asdict(data) for data in value]  # type: ignore

    CONSOLE.print(to_print_dict)


def print_base_network_data_json(network_data: "BaseNetworkData", *args, **kwargs):
    from dataclasses import asdict

    CONSOLE.print(asdict(network_data))
