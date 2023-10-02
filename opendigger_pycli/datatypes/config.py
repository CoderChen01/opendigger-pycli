import typing as t
from dataclasses import dataclass


@dataclass
class BaseConfig:
    config_name: t.ClassVar[str]


@dataclass
class AppKeyConfig(BaseConfig):
    config_name: t.ClassVar[str] = "app_keys"
    openai_key: str = "None"
    github_pat: str = "None"


@dataclass
class UserInfoConfig(BaseConfig):
    config_name: t.ClassVar[str] = "user_info"
    name: str = "Unknown"
    email: str = "Unknown"


ALL_CONFIGS: t.Dict[str, t.Type[BaseConfig]] = {
    "app_keys": AppKeyConfig,
    "user_info": UserInfoConfig,
}
