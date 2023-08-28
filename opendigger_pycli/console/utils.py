import typing as t


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        NameAndValue,
        NameNameAndValue,
    )


def if_prettey(value: t.Any) -> bool:
    if isinstance(value, list):
        if hasattr(value[0], "name"):
            value = t.cast(t.List["NameAndValue"], value)
            return True
        if hasattr(value[0], "name0"):
            value = t.cast(t.List["NameNameAndValue"], value)
            return True
    return False
