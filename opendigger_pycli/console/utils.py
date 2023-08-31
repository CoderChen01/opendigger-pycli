import typing as t

from . import CONSOLE

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import NameAndValue, NameNameAndValue
    from opendigger_pycli.datatypes.query import IndicatorQuery


def if_prettey(value: t.Any) -> bool:
    if isinstance(value, list):
        if hasattr(value[0], "name"):
            value = t.cast(t.List["NameAndValue"], value)
            return True
        if hasattr(value[0], "name0"):
            value = t.cast(t.List["NameNameAndValue"], value)
            return True
    return False


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
