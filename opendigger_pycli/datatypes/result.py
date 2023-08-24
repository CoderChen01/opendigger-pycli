import typing as t
from dataclasses import dataclass, field


@dataclass
class BaseUserResult:
    type: t.ClassVar[str] = "user"
    username: str
    retrival_metric_names: t.List[str] = field(default_factory=list)

    def add_metric_names(self, metric_names: t.List[str]):
        self.retrival_metric_names.extend(metric_names)


@dataclass
class BaseRepoResult:
    type: t.ClassVar[str] = "repo"
    repo: str
    retrival_metric_names: t.List[str] = field(default_factory=list)
    org_name: str = field(init=False)
    repo_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.org_name, self.repo_name = self.repo.split("/")
