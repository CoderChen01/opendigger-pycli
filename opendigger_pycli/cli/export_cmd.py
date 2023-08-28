import typing as t

import click

from .base import pass_environment
from ..utils.decorators import processor

if t.TYPE_CHECKING:
    from .base import Environment


@click.command("export", help="Export metrics")
@click.option(
    "--format",
    "-f",
    "format_name",
    type=click.Choice(["csv", "json", "mhtml"]),
    required=True,
)
@click.option("--filename", "-o", "filename", type=str, required=True)
@processor
@pass_environment
def export(
    env: "Environment",
    format_name: t.Literal["csv", "json", "mhtml"],
    filename: click.Path,
):
    pass
