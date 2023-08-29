import typing as t
from dataclasses import dataclass

T = t.TypeVar("T")


@dataclass
class DataloaderResult(t.Generic[T]):
    is_success: bool
    dataloader: "DataloaderProto"
    desc: str
    data: t.Optional[T] = None

    def __repr__(self) -> str:
        data_class_name = "None" if self.data is None else self.data.__class__.__name__
        return (
            f"{self.dataloader.__class__.__name__}State("
            f"is_success={self.is_success}, "
            f"desc='{self.desc}', "
            f"data={data_class_name}())"
        )


@t.runtime_checkable
class DataloaderProto(t.Protocol):
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    indicator_type: t.ClassVar[
        t.Literal["index", "metric", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]]
    demo_url: t.ClassVar[str]

    def load(self, *args, **kwargs) -> DataloaderResult:
        ...
