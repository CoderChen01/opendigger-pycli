import typing as t
from pathlib import Path

import click

from opendigger_pycli.console.print_indicator import SURPPORTED_DISPLAY_FORMATS
from opendigger_pycli.results.display import DisplyCMDResult
from opendigger_pycli.utils.decorators import processor

from ..base import pass_environment

if t.TYPE_CHECKING:
    from opendigger_pycli.console.print_indicator import SURPPORTED_DISPLAY_FORMAT_TYPE
    from opendigger_pycli.results.query import QueryResults

    from ..base import Environment


@click.command("display", help="Display indicators in terminal")
@click.option(
    "--format",
    "-f",
    "format_name",
    type=click.Choice(SURPPORTED_DISPLAY_FORMATS),
    help="Display format",
    required=True,
)
@click.option(
    "--save",
    "-s",
    "save_path",
    type=click.Path(resolve_path=True, path_type=Path, file_okay=False),
    help="Save output to file, you can use this option get a simple report",
)
@click.option(
    "--paging/--no-paging",
    "-p/ ",
    "paging",
    default=False,
    help="Page output like more/less command, "
    "you CANNOT use this option and save to file at the same time",
)
@click.option(
    "--pager-color/--no-pager-color",
    "-c/ ",
    "pager_color",
    default=True,
    help="Enable color in pager, Only works when paging is enabled",
)
@processor
@pass_environment
def display(
    env: "Environment",
    results: "QueryResults",
    format_name: "SURPPORTED_DISPLAY_FORMAT_TYPE",
    save_path: t.Optional[Path],
    paging: bool,
    pager_color: bool,
):
    env.dlog(f"Received Params: format_name={format_name}, save_path={save_path}")
    env.vlog(f"Displaying results, format: {format_name}")
    DisplyCMDResult(
        results, format_name, save_path, paging=paging, color=pager_color
    ).display()
    yield from results
