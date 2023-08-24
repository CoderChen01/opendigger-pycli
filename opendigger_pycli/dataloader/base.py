import abc
import itertools
import typing as t

from opendigger_pycli.datatypes import DataloaderState, DataloaderProto


DATALOADERS = t.TypedDict(
    "DATALOADERS",
    index=t.Dict[str, t.Type[DataloaderProto]],
    metric=t.Dict[str, t.Type[DataloaderProto]],
    network=t.Dict[str, t.Type[DataloaderProto]],
)(index={}, metric={}, network={})


T = t.TypeVar("T")


def register_dataloader(
    cls: t.Union[
        t.Type["BaseRepoDataloader"],
        t.Type["BaseUserDataloader"],
        t.Type["BaseOpenRankNetworkDataloader"],
    ]
):
    DATALOADERS[cls.metric_type][cls.name] = t.cast(
        t.Type[DataloaderProto], cls
    )
    return cls


def filter_dataloader(
    types: t.Set[t.Literal["repo", "user"]],
    metric_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
) -> t.Iterator[DataloaderProto]:
    metric_dicts: t.Iterator[t.Dict[str, t.Type[DataloaderProto]]] = (
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


class BaseRepoDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    metric_type: t.ClassVar[
        t.Literal["index", "metric", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]] = "repo"

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str) -> DataloaderState[T]:
        pass


class BaseOpenRankNetworkDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    metric_type: t.ClassVar[
        t.Literal["network"]
    ] = "network"  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]]

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str, date: str):
        pass


class BaseUserDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    metric_type: t.ClassVar[
        t.Literal["index", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]] = "user"

    @abc.abstractmethod
    def load(self, username: str):
        pass
