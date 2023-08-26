import typing as t
from dataclasses import dataclass, field

from .dataloader import DataloaderProto


@dataclass
class BaseResult:
    type: t.ClassVar[t.Literal["user", "repo"]]
    dataloaders: t.List[DataloaderProto]
    data: t.Dict[str, t.Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        pass


@dataclass
class BaseUserResult(BaseResult):
    type: t.ClassVar[t.Literal["user"]] = "user"
    username: str


@dataclass
class BaseRepoResult(BaseResult):
    type: t.ClassVar[t.Literal["repo"]] = "repo"
    repo: t.Tuple[str, str]
    org_name: str = field(init=False)
    repo_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.org_name, self.repo_name = self.repo
