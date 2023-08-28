import typing as t

from rich.pretty import Pretty


from . import CONSOLE
from .utils import if_prettey

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        BaseNetworkData,
    )


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


def print_base_network_data_json(
    network_data: "BaseNetworkData", *args, **kwargs
):
    pass
