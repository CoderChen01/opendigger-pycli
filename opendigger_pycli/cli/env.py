import os
import textwrap
import typing as t

import click

from opendigger_pycli.config.cli_config import OpenDiggerCliConfig
from opendigger_pycli.console import CONSOLE


if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.dataloader import DataloaderProto


class Environment:
    verbose: bool
    home: str
    cli_config: OpenDiggerCliConfig
    mode: t.Literal["repo", "user"]
    params: t.Union[t.List[t.Tuple[str, str]], t.List[str]]

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
        self.params = []

        self.load_configs()

    def log(self, msg):
        """Logs a message"""
        if isinstance(msg, str):
            msg = textwrap.dedent(msg)
        CONSOLE.log(msg)

    def vlog(self, *msgs):
        """Logs a message only if verbose is enabled."""
        if not self.verbose:
            return

        for msg in msgs:
            self.log(msg)

    def load_configs(self) -> bool:
        try:
            if self.verbose:
                with CONSOLE.status("[bold green]loading configs..."):
                    self.cli_config = OpenDiggerCliConfig()
                self.cli_config.print()
            else:
                self.cli_config = OpenDiggerCliConfig()
            return True
        except Exception as e:
            self.log(f"[bold red]load configs failed: {e}")
            return False

    def set_mode(self, mode: t.Literal["repo", "user"]) -> None:
        self.mode = mode

    def set_params(
        self, params: t.Union[t.List[t.Tuple[str, str]], t.List[str]]
    ) -> None:
        self.params = params
