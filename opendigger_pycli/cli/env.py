import logging
import os
import textwrap
import typing as t

import click
from rich.logging import RichHandler

from opendigger_pycli.config import OpenDiggerCliConfig
from opendigger_pycli.console import CONSOLE

FORMAT = "%(message)s"
RICH_LOGGER_HANDLER = RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])
logging.basicConfig(
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RICH_LOGGER_HANDLER],
)


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
        self.logger = logging.getLogger("opendigger-pycli")

    def log(
        self,
        msg,
        mode: t.Literal["info", "warn", "debug", "error"] = "info",
    ):
        """Logs a message"""
        if isinstance(msg, str):
            msg = textwrap.dedent(msg)

        if mode == "info":
            self.logger.info(msg, extra={"markup": True, "expand": True})
        elif mode == "warn":
            self.logger.warning(msg, extra={"markup": True, "expand": True})
        elif mode == "debug":
            self.logger.debug(msg, extra={"markup": True, "expand": True})
        else:
            self.logger.error(msg, extra={"markup": True, "expand": True})

    def vlog(self, *msgs):
        """Logs a message only if verbose is enabled."""
        if not self.verbose:
            return
        for msg in msgs:
            self.log(msg)

    def elog(self, *msg):
        if not self.verbose:
            return
        for m in msg:
            self.log(m, "error")

    def wlog(self, *msg):
        if not self.verbose:
            return
        for m in msg:
            self.log(m, "warn")

    def dlog(self, *msg):
        if not self.verbose:
            return
        for m in msg:
            self.log(m, "debug")

    def load_configs(self) -> bool:
        try:
            self.vlog("[bold green]loading configs...")
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

    def set_log_level(
        self,
        log_level: t.Optional[
            t.Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        ] = None,
    ) -> None:
        if log_level is None:
            self.verbose = False
        else:
            self.verbose = True
            self.logger.setLevel(log_level)
            RICH_LOGGER_HANDLER.setLevel(log_level)
            CONSOLE.quiet = True
            self.log("[bold green]verbose mode enabled")

        self.load_configs()

    def set_config(self, section_name: str, key: str, value: str) -> None:
        config = getattr(self.cli_config, section_name.replace(".", "_"))
        setattr(config, key, value)
        self.cli_config.update_config()
        self.dlog(
            f"[bold green]set config {section_name}.{key} to {value} successfully"
        )
