import typing as t
from dataclasses import dataclass


@dataclass
class BaseConfig:
    config_name: t.ClassVar[str]


@dataclass
class AppKeyConfig(BaseConfig):
    config_name: t.ClassVar[str] = "app_keys"
    openai_key: str = ""
    github_pat: str = ""


@dataclass
class UserInfoConfig(BaseConfig):
    config_name: t.ClassVar[str] = "user_info"
    name: str = ""
    email: str = ""


ALL_CONFIGS: t.List[t.Type[BaseConfig]] = [AppKeyConfig, UserInfoConfig]
