import typing as t
from dataclasses import dataclass

T = t.TypeVar("T")


@dataclass
class DataloaderState(t.Generic[T]):
    is_success: bool
    desc: str
    data: t.Optional[T] = None


@t.runtime_checkable
class DataloaderProto(t.Protocol):
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    metric_type: t.ClassVar[
        t.Literal["index", "metric", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]]
    demo_url: t.ClassVar[str]

    def load(self, *args, **kwargs) -> DataloaderState:
        ...
