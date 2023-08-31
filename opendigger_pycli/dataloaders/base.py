import abc
import itertools
import typing as t
from collections import defaultdict

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import DataloaderProto


class DataLoadersType(t.TypedDict):
    index: t.Dict[str, t.List[t.Type["DataloaderProto"]]]
    metric: t.Dict[str, t.List[t.Type["DataloaderProto"]]]
    network: t.Dict[str, t.List[t.Type["DataloaderProto"]]]


DATALOADERS = DataLoadersType(
    index=defaultdict(list),
    metric=defaultdict(list),
    network=defaultdict(list),
)


T = t.TypeVar("T")


def register_dataloader(
    cls: t.Union[
        t.Type["BaseRepoDataloader"],
        t.Type["BaseUserDataloader"],
        t.Type["BaseOpenRankNetworkDataloader"],
    ]
):
    DATALOADERS[cls.indicator_type][cls.name].append(
        t.cast(t.Type["DataloaderProto"], cls)
    )
    return cls


def filter_dataloader(
    types: t.Set[t.Literal["repo", "user"]],
    indicator_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
) -> t.Iterator["DataloaderProto"]:
    indicator_dicts: t.List[t.Dict[str, t.List[t.Type["DataloaderProto"]]]] = list(
        t.cast(
            t.ValuesView,
            DATALOADERS.values(),
        )
    )
    indicator_dataloaders = itertools.chain.from_iterable(
        itertools.chain.from_iterable(
            [
                [
                    indicator_dataloader()
                    for indicator_dataloader in indicator_dataloaders
                    if (
                        indicator_dataloader.type in types
                        and not indicator_types
                        and indicator_dataloader.introducer in introducers
                    )
                    or (
                        indicator_dataloader.type in types
                        and indicator_dataloader.indicator_type in indicator_types
                        and not introducers
                    )
                    or (
                        indicator_dataloader.type in types
                        and indicator_dataloader.indicator_type in indicator_types
                        and indicator_dataloader.introducer in introducers
                    )
                ]
                for indicator_dataloaders in indicator_dict.values()
            ]
            for indicator_dict in indicator_dicts
        )
    )
    return indicator_dataloaders


class BaseRepoDataloader(abc.ABC):
    # Specify the name of the indicator,
    # which is different from the name field in datatypes
    name: t.ClassVar[str]
    pass_date: t.ClassVar[bool] = False
    indicator_type: t.ClassVar[
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
    indicator_type: t.ClassVar[
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
    indicator_type: t.ClassVar[
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
