from dataclasses import dataclass, field
import typing as t


@dataclass(frozen=True)
class MetricQuery:
    months: t.FrozenSet[int] = field(default_factory=frozenset)
    years: t.FrozenSet[int] = field(default_factory=frozenset)
    year_months: t.FrozenSet[t.Tuple[int, int]] = field(
        default_factory=frozenset
    )
