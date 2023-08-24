import os
import typing as t

import click

from opendigger_pycli.config.cli_config import OpenDiggerCliConfig
from opendigger_pycli.console import CONSOLE


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
        CONSOLE.log(msg)

    def vlog(self, msg):
        """Logs a message only if verbose is enabled."""
        if self.verbose:
            CONSOLE.log(msg)

    def load_configs(self):
        if self.verbose:
            with CONSOLE.status("[bold green]loading configs..."):
                self.cli_config = OpenDiggerCliConfig()
            self.cli_config.print()
        else:
            self.cli_config = OpenDiggerCliConfig()

    def set_mode(self, mode: t.Literal["repo", "user"]):
        self.mode = mode

    def set_params(
        self, params: t.Union[t.List[t.Tuple[str, str]], t.List[str]]
    ):
        self.params = params
