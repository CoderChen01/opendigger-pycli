import typing as t

import click

from .base import pass_environment
from ..utils.decorators import processor

if t.TYPE_CHECKING:
    from .base import Environment


@click.command("display", help="Display metrics")
@click.option(
    "--format",
    "-f",
    "format_name",
    type=click.Choice(["table", "json", "object"]),
    required=True,
)
@processor
@pass_environment
def display(env: "Environment", results, format_name):
    env.vlog("Display Results")

    yield from results
