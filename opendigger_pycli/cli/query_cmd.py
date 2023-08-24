import typing as t

import click

from opendigger_pycli.query.base import QueryRepoResult, QueryUserResult
from opendigger_pycli.console.print_base_info import print_metric_info
from .base import pass_environment, Environment
from .custom_types import (
    INDEX_NAME_TYPE,
    METRIC_NAME_TYPE,
    NETWORK_NAME_TYPE,
    ALL_METRIC_NAMES_TYPE,
)


@click.group(
    "query", chain=True, help="Query metrics", invoke_without_command=True
)
@click.option(
    "--ignore",
    "-i",
    "ignore_metric_names",
    multiple=True,
    type=ALL_METRIC_NAMES_TYPE,
    help="The metrics to ignore.",
    required=False,
)
@click.option(
    "--select",
    "-s",
    "select_metric_names",
    multiple=True,
    type=ALL_METRIC_NAMES_TYPE,
    help="The metrics to select.",
    required=False,
)
@click.option("--all", "-a", "is_all", is_flag=True, default=False)
@click.option(
    "--index",
    "-i",
    "index_names",
    multiple=True,
    type=INDEX_NAME_TYPE,
    help="Select metrics whose type is INDEX.",
    required=False,
)
@click.option(
    "--metric",
    "-m",
    "metric_names",
    multiple=True,
    type=METRIC_NAME_TYPE,
    help="Select metrics whose type is METRIC.",
    required=False,
)
@click.option(
    "--network",
    "-n",
    "network_names",
    multiple=True,
    type=NETWORK_NAME_TYPE,
    help="Select metrics whose type is NETWORK.",
    required=False,
)
@click.option(
    "--x-lab",
    "-x",
    "x_lab_metric_names",
    multiple=True,
    type=NETWORK_NAME_TYPE,
    help="Select metrics whose introducer is X-lab.",
    required=False,
)
@click.option(
    "--chaoss",
    "-c",
    "choass_metric_names",
    multiple=True,
    type=NETWORK_NAME_TYPE,
    help="Select metrics whose introducer is CHAOSS.",
    required=False,
)
@pass_environment
def query(
    env: Environment,
    ignore_metric_names: t.Optional[t.List[str]],
    select_metric_names: t.Optional[t.List[str]],
    is_all: bool,
    index_names: t.Optional[t.List[str]],
    network_names: t.Optional[t.List[str]],
    metric_names: t.Optional[t.List[str]],
    x_lab_metric_names: t.Optional[t.List[str]],
    choass_metric_names: t.Optional[t.List[str]],
):
    """
    Query Metrics

    if you don't specify any options, all metric name will be displayed
    if --all is set, all metrics will be queried
    """
    if click.get_current_context().invoked_subcommand is None:
        print_metric_info(
            types={"repo", "user"},
            metric_types={"index", "metric", "network"},
            introducers={"X-lab", "CHAOSS"},
        )


@click.command("export", help="Export metrics")
@click.option("--format", "-f", "format_name", type=str, required=True)
@click.option("--filename", "-o", "filename", type=str, required=True)
def export(format_name, filename):
    pass


@click.command("display", help="Display metrics")
@click.option("--format", "-f", "format_name", type=str, required=True)
def display(format_name):
    pass
