import typing as t
from dataclasses import dataclass, field


@dataclass(frozen=True)
class IndicatorQuery:
    months: t.FrozenSet[int] = field(default_factory=frozenset)
    years: t.FrozenSet[int] = field(default_factory=frozenset)
    year_months: t.FrozenSet[t.Tuple[int, int]] = field(default_factory=frozenset)
