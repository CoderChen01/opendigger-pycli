import abc
import itertools
import typing as t

from opendigger_pycli.datatypes import DataloaderState, DataloaderProto


DATALOADERS = t.TypedDict(
    "DATALOADERS",
    index=t.Dict[str, DataloaderProto],
    metric=t.Dict[str, DataloaderProto],
    network=t.Dict[str, DataloaderProto],
)(index={}, metric={}, network={})


T = t.TypeVar("T")


def register_dataloader(cls: DataloaderProto):
    DATALOADERS[cls.metric_type][cls.name] = cls
    return cls


def filter_dataloader(
    types: t.Set[t.Literal["repo", "user"]],
    metric_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
) -> t.Iterator[DataloaderProto]:
    metric_dicts: t.Iterator[t.Dict[str, DataloaderProto]] = (
        DATALOADERS[metric_type] for metric_type in metric_types
    )
    metric_dataloaders = itertools.chain.from_iterable(
        (
            (
                metric_dataloder
                for metric_dataloder in metric_dict.values()
                if metric_dataloder.type in types
                and metric_dataloder.introducer in introducers
            )
            for metric_dict in metric_dicts
        )
    )
    return metric_dataloaders


class BaseRepoDataloader(abc.ABC, t.Generic[T]):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: str
    metric_type: t.Literal[
        "index", "metric", "network"
    ]  # Specifies the type of indicator
    introducer: str
    type: str = "repo"

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str) -> DataloaderState[T]:
        pass


class BaseOpenRankNetworkDataloader(abc.ABC, t.Generic[T]):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: str
    metric_type: t.Literal["network"]  # Specifies the type of indicator
    introducer: str
    type: str

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str, date: str) -> DataloaderState[T]:
        pass


class BaseUserDataloader(abc.ABC, t.Generic[T]):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: str
    metric_type: t.Literal[
        "index", "network"
    ]  # Specifies the type of indicator
    introducer: str
    type: str = "user"

    @abc.abstractmethod
    def load(self, username: str) -> DataloaderState[T]:
        pass
