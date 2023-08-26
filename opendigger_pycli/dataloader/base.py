import abc
from collections import defaultdict
import itertools
import typing as t


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import DataloaderProto


DATALOADERS = t.TypedDict(
    "DATALOADERS",
    index=t.Dict[str, t.List[t.Type["DataloaderProto"]]],
    metric=t.Dict[str, t.List[t.Type["DataloaderProto"]]],
    network=t.Dict[str, t.List[t.Type["DataloaderProto"]]],
)(index=defaultdict(list), metric=defaultdict(list), network=defaultdict(list))


T = t.TypeVar("T")


def register_dataloader(
    cls: t.Union[
        t.Type["BaseRepoDataloader"],
        t.Type["BaseUserDataloader"],
        t.Type["BaseOpenRankNetworkDataloader"],
    ]
):
    DATALOADERS[cls.metric_type][cls.name].append(
        t.cast(t.Type["DataloaderProto"], cls)
    )
    return cls


def filter_dataloader(
    types: t.Set[t.Literal["repo", "user"]],
    metric_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
) -> t.Iterator["DataloaderProto"]:
    metric_dicts: t.List[
        t.Dict[str, t.List[t.Type["DataloaderProto"]]]
    ] = list(
        t.cast(
            t.ValuesView,
            DATALOADERS.values(),
        )
    )
    metric_dataloaders = itertools.chain.from_iterable(
        itertools.chain.from_iterable(
            [
                [
                    metric_dataloader()
                    for metric_dataloader in metric_dataloaders
                    if (
                        metric_dataloader.type in types
                        and not metric_types
                        and metric_dataloader.introducer in introducers
                    )
                    or (
                        metric_dataloader.type in types
                        and metric_dataloader.metric_type in metric_types
                        and not introducers
                    )
                    or (
                        metric_dataloader.type in types
                        and metric_dataloader.metric_type in metric_types
                        and metric_dataloader.introducer in introducers
                    )
                ]
                for metric_dataloaders in metric_dict.values()
            ]
            for metric_dict in metric_dicts
        )
    )
    return metric_dataloaders


class BaseRepoDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    metric_type: t.ClassVar[
        t.Literal["index", "metric", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]] = "repo"
    demo_url: t.ClassVar[str]

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class BaseOpenRankNetworkDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    metric_type: t.ClassVar[
        t.Literal["network"]
    ] = "network"  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]]
    demo_url: t.ClassVar[str]

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def load(self, org: str, repo: str, dates: t.List[t.Tuple[int, int]]):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class BaseUserDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    metric_type: t.ClassVar[
        t.Literal["index", "network"]
    ]  # Specifies the type of indicator
    introducer: t.ClassVar[t.Literal["X-lab", "CHAOSS"]]
    type: t.ClassVar[t.Literal["repo", "user"]] = "user"
    demo_url: t.ClassVar[str]

    @abc.abstractmethod
    def load(self, username: str):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
