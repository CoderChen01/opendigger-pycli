import typing as t
from collections import defaultdict

import click

from opendigger_pycli.results.query import QueryRepoResult, QueryUserResult
from opendigger_pycli.console.print_base_info import print_metric_info
from opendigger_pycli.console import CONSOLE
from opendigger_pycli.dataloader import filter_dataloader
from .base import pass_environment
from .custom_types import FILTERED_METRIC_QUERY_TYPE, IGNORED_METRIC_NAME_TYPE

if t.TYPE_CHECKING:
    from click import Context

    from opendigger_pycli.datatypes import MetricQuery
    from .base import Environment


def update_filtered_metric_dataloaders(ctx: "Context") -> None:
    if "metric_types" in ctx.params and ctx.params["metric_types"]:
        metric_types = ctx.params["metric_types"]
    else:
        metric_types = {"index", "metric", "network"}

    if "introducers" in ctx.params and ctx.params["introducers"]:
        introducers = ctx.params["introducers"]
    else:
        introducers = {"X-lab", "CHAOSS"}
    dataloaders = filter_dataloader(
        {
            t.cast(
                t.Literal["repo", "user"],
                t.cast("Context", ctx.parent).command.name,
            )
        },
        t.cast(
            t.Set[t.Literal["index", "metric", "network"]],
            metric_types,
        ),
        t.cast(t.Set[t.Literal["X-lab", "CHAOSS"]], introducers),
    )
    ctx.meta[f"{__name__}.filtered_dataloaders"] = {
        dataloader.name: dataloader for dataloader in dataloaders
    }


def add_metric_type(
    ctx: click.Context,
    param: click.Parameter,
    value: t.Literal["index", "metric", "network"],
) -> None:
    if "metric_types" in ctx.params:
        if value is None:
            return
        if isinstance(ctx.params["metric_types"], set):
            ctx.params["metric_types"].add(value)
        else:
            ctx.params["metric_types"] = set()
            ctx.params["metric_types"].add(value)
    elif value is not None:
        ctx.params["metric_types"] = set()
        ctx.params["metric_types"].add(value)
    else:
        ctx.params["metric_types"] = set()
    update_filtered_metric_dataloaders(ctx)


def add_introducer(
    ctx: click.Context,
    param: click.Parameter,
    value: t.Literal["X-lab", "CHAOSS"],
) -> None:
    if "introducers" in ctx.params:
        if value is None:
            return
        if isinstance(ctx.params["introducers"], set):
            ctx.params["introducers"].add(value)
        else:
            ctx.params["introducers"] = set()
            ctx.params["introducers"].add(value)
    elif value is not None:
        ctx.params["introducers"] = set()
        ctx.params["introducers"].add(value)
    else:
        ctx.params["introducers"] = set()

    update_filtered_metric_dataloaders(ctx)


def distinct_metric_queries(
    metric_quries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]]
) -> t.List[t.Tuple[str, t.Optional["MetricQuery"]]]:
    metric_query_dict = defaultdict(list)
    for metric_query in metric_quries:
        metric_name, query = metric_query
        metric_query_dict[metric_name].append(query)

    new_metric_queries = []
    for metric_name, queries in metric_query_dict.items():
        queries = set(queries)
        for query in queries:
            new_metric_queries.append((metric_name, query))

    return new_metric_queries


def distinct_metric_names(metric_names: t.List[str]) -> t.List[str]:
    return list(set(metric_names))


@click.group(
    "query", chain=True, help="Query metrics", invoke_without_command=True
)
@click.option(
    "--index",
    "-i",
    "index_flag",
    flag_value="index",
    help="Select metrics whose type is INDEX.",
    default=False,
    callback=add_metric_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--metric",
    "-m",
    "metric_flag",
    flag_value="metric",
    help="Select metrics whose type is METRIC.",
    default=False,
    callback=add_metric_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--network",
    "-n",
    "network_flag",
    flag_value="network",
    help="Select metrics whose type is NETWORK.",
    default=False,
    callback=add_metric_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--x-lab",
    "-x",
    "x_lab_flag",
    flag_value="X-lab",
    help="Select metrics whose introducer is X-lab.",
    default=False,
    callback=add_introducer,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--chaoss",
    "-c",
    "chaoss_flag",
    flag_value="CHAOSS",
    help="Select metrics whose introducer is CHAOSS.",
    default=False,
    callback=add_introducer,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--select",
    "-s",
    "selected_metric_queries",
    type=FILTERED_METRIC_QUERY_TYPE,
    multiple=True,
    help="The metrics to select.",
    required=False,
)
@click.option(
    "--only-select/--no-only-select",
    "-o/-N",
    "is_only_select",
    is_flag=True,
    default=True,
    help="Only query selected metrics.",
)
@click.option(
    "--ignore",
    "-I",
    "ignore_metric_names",
    multiple=True,
    type=IGNORED_METRIC_NAME_TYPE,
    help="The metrics to ignore.",
    required=False,
)
@pass_environment
def query(
    env: "Environment",
    metric_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
    selected_metric_queries: t.List[t.Tuple[str, t.Optional["MetricQuery"]]],
    is_only_select: bool,
    ignore_metric_names: t.List[str],
):
    """
    Query Metrics

    if you don't specify any options, all metric name will be displayed
    if --all is set, all metrics will be queried
    """
    # Processing parameters: deduplication and default value processing
    selected_metric_queries = distinct_metric_queries(selected_metric_queries)
    ignore_metric_names = distinct_metric_names(ignore_metric_names)
    if not metric_types and not introducers:
        metric_types = {"index", "metric", "network"}
        introducers = {"X-lab", "CHAOSS"}

    env.vlog(
        f"""Parameters:
        metric_types: {metric_types},
        introducers: {introducers}, 
        selected_metric_queries: {selected_metric_queries}, 
        is_only_select: {is_only_select},
        ignore_metric_names: {ignore_metric_names}
        """
    )

    # If the subcommand is not called, then print the filtered metrics information
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("Loading metrics info..."):
            print_metric_info(
                mode=env.mode,
                metric_types=t.cast(
                    t.Set[t.Literal["index", "metric", "network"]],
                    metric_types,
                ),
                introducers=t.cast(
                    t.Set[t.Literal["X-lab", "CHAOSS"]], introducers
                ),
            )
            return

    # If the subcommand is called, then query the metrics，
    # and get the filtered dataloaders initialized at option callback in the context
    filtered_dataloaders = click.get_current_context().meta[
        f"{__name__}.filtered_dataloaders"
    ]

    # Query only selected metrics
    if is_only_select:
        env.vlog("Query only selected metrics")
        dataloaders = [
            filtered_dataloaders[metric_name]
            for metric_name, _ in selected_metric_queries
        ]
    else:  # Query all metrics
        env.vlog("Query all metrics")
        dataloaders = list(filtered_dataloaders.values())

    mode = env.mode  # This is assigned in the repo command
    if mode == "user":
        usernames = t.cast(t.List[str], env.params)
        # build result
        results = [
            QueryUserResult(
                username=username,
                dataloaders=dataloaders,
                metric_queries=selected_metric_queries,
            )
            for username in usernames
        ]

    # repo mode
    repos = t.cast(t.List[t.Tuple[str, str]], env.params)
    # build result
    results = [
        QueryRepoResult(
            repo=repo,
            dataloaders=dataloaders,
            metric_queries=selected_metric_queries,
        )
        for repo in repos
    ]

    env.vlog("Query Results:", results)

    # add result to context
    env.add_query_results(results)
    env.vlog(
        f"Save Query Results to Context Meta: {'[green]Success[/]' if env.get_query_results() is not None else '[red]Error[/]'}"
    )


@query.command("export", help="Export metrics")
@click.option("--format", "-f", "format_name", type=str, required=True)
@click.option("--filename", "-o", "filename", type=str, required=True)
def export(format_name, filename):
    pass


@query.command("display", help="Display metrics")
@click.option("--format", "-f", "format_name", type=str, required=True)
def display(format_name):
    pass
