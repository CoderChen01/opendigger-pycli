import configparser
import typing as t
from dataclasses import fields, is_dataclass
from pathlib import Path

import click
from rich import box
from rich.table import Table

from opendigger_pycli.datatypes import ALL_CONFIGS, AppKeyConfig, UserInfoConfig

if t.TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


class OpenDiggerCliConfig:
    app_keys: AppKeyConfig
    user_info: UserInfoConfig

    def __init__(self):
        self.__load_config()

    @property
    def user_config_file_path(self) -> str:
        config_dir_str = click.get_app_dir("opendigger-pycli")
        config_dir = Path(config_dir_str)
        config_dir.mkdir(parents=True, exist_ok=True)
        user_config = config_dir / "config.ini"
        if not user_config.exists():
            user_config.touch()
        return str(user_config)

    @property
    def default_config_file_path(self) -> str:
        default_config = Path(__file__).with_name("default_config.ini")
        return str(default_config)

    @property
    def config_file_paths(self) -> t.List[str]:
        return [str(self.default_config_file_path), str(self.user_config_file_path)]

    def __load_config(self):
        parser = configparser.RawConfigParser()
        parser.read(self.config_file_paths)

        for config_dataclass_key in ALL_CONFIGS:
            config_dataclass = ALL_CONFIGS[config_dataclass_key]
            if not is_dataclass(config_dataclass):
                raise TypeError(f"{config_dataclass} is not a dataclass")

            setattr(self, config_dataclass.config_name, config_dataclass())
            config_fields = fields(config_dataclass)
            for field in config_fields:
                data = parser.get(
                    config_dataclass.config_name, field.name, fallback=field.default
                )
                setattr(getattr(self, config_dataclass.config_name), field.name, data)

    def update_config(self):
        parser = configparser.RawConfigParser()
        parser.read(self.config_file_paths)

        for config_dataclass_key in ALL_CONFIGS:
            config_dataclass = ALL_CONFIGS[config_dataclass_key]
            if not is_dataclass(config_dataclass):
                raise TypeError(f"{config_dataclass} is not a dataclass")

            config = getattr(self, config_dataclass.config_name, config_dataclass())
            config_fields = fields(config_dataclass)
            for field in config_fields:
                parser.set(
                    config_dataclass.config_name,
                    field.name,
                    getattr(config, field.name),
                )

        with open(self.user_config_file_path, "w") as file:
            parser.write(file)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        yield "[b]OpenDigger Python CLI Configs:[/b]"
        for config_dataclass_key in ALL_CONFIGS:
            config_dataclass = ALL_CONFIGS[config_dataclass_key]
            if not is_dataclass(config_dataclass):
                raise TypeError(f"{config_dataclass} is not a dataclass")

            table = Table(
                "Key", "Value", title=config_dataclass.config_name, box=box.HORIZONTALS  # type: ignore
            )
            config = getattr(self, config_dataclass.config_name, config_dataclass())  # type: ignore
            config_fields = fields(config_dataclass)
            for field in config_fields:
                table.add_row(field.name, getattr(config, field.name))
            yield table
