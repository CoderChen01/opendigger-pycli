from __future__ import annotations
import typing as t

from .config import OpenDiggerCliConfig

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.config import UserInfoConfig


def get_github_pat() -> str:
    return OpenDiggerCliConfig().app_keys.github_pat


def has_github_pat() -> bool:
    return get_github_pat() != "None"


def get_user_info() -> UserInfoConfig:
    return OpenDiggerCliConfig().user_info
