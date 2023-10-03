from __future__ import annotations
import typing as t
import click

from opendigger_pycli.console import CONSOLE
from opendigger_pycli.utils.decorators import processor


if t.TYPE_CHECKING:
    from opendigger_pycli.results.query import QueryResults


@click.command("print-result", help="[Plugin Demo] Print query result to terminal")
@processor
def print_result(results: QueryResults):
    CONSOLE.print(results)
    yield from results
