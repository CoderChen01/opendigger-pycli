import typing as t
from pathlib import Path

import click

from opendigger_pycli.exporters import (
    CAN_SPLIT_EXPORT_FORMATS,
    SURPPORTED_EXPORT_FORMAT_TYPE,
    SURPPORTED_EXPORT_FORMATS,
)
from opendigger_pycli.results.export import ExportResult
from opendigger_pycli.utils.decorators import processor

from ..base import pass_environment

if t.TYPE_CHECKING:
    from opendigger_pycli.results.query import QueryResults

    from ..base import Environment


@click.command("export", help="Export metrics")
@click.option(
    "--format",
    "-f",
    type=click.Choice(SURPPORTED_EXPORT_FORMATS),
    required=True,
    help="Format to export",
)
@click.option(
    "--save-dir",
    "-s",
    "save_dir",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Directory to save indicators",
)
@click.option(
    "--split/--no-split",
    "is_split",
    default=False,
    is_flag=True,
    help="Save indicators in separate files, ONLY For JSON format",
)
@processor
@pass_environment
def export(
    env: "Environment",
    results: "QueryResults",
    format: SURPPORTED_EXPORT_FORMAT_TYPE,
    save_dir: Path,
    is_split: bool,
):
    if is_split and format not in CAN_SPLIT_EXPORT_FORMATS:
        raise click.BadParameter(f"This format {format} does not support split")

    ExportResult(results, format, save_dir, is_split).export()
    yield from results
