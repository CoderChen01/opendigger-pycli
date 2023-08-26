import typing as t

import click

from opendigger_pycli.console.print_base_info import (
    print_repo_info,
    print_user_info,
)
from opendigger_pycli.console import CONSOLE
from opendigger_pycli.results.query import QueryRepoResult, QueryUserResult
from opendigger_pycli.console.print_base_info import print_indicator_info
from opendigger_pycli.utils.decorators import (
    process_commands,
    pass_filtered_dataloaders,
)

from .env import Environment
from .custom_types import (
    GH_REPO_NAME_TYPE,
    GH_USERNAME_TYPE,
    FILTERED_METRIC_QUERY_TYPE,
    IGNORED_METRIC_NAME_TYPE,
)
from .utils import (
    add_introducer,
    add_indicator_type,
    distinct_indicator_names,
    distinct_indicator_queries,
)


if t.TYPE_CHECKING:
    from click import Group
    from opendigger_pycli.datatypes import IndicatorQuery, DataloaderProto
    from .base import Environment


pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enables verbose mode.",
)
@pass_environment
def opendigger(env: Environment, verbose: bool):
    """Open Digger CLI"""
    env.verbose = verbose


opendigger_cmd = t.cast("Group", opendigger)


@opendigger_cmd.group(invoke_without_command=True)
@click.option(
    "--username",
    "-u",
    "usernames",
    type=GH_USERNAME_TYPE,
    multiple=True,
    help="GitHub username",
)
@pass_environment
def user(env: Environment, usernames: t.List[str]):
    """
    Operate on user indicators
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]requesting users info..."):
            print_user_info(usernames, env.cli_config.github_pat)
    else:
        env.set_mode("user")
        env.set_params(usernames)


@opendigger_cmd.group(invoke_without_command=True)
@click.option(
    "--repo",
    "-r",
    "repos",
    type=GH_REPO_NAME_TYPE,
    multiple=True,
    help="GitHub repository, e.g. X-lab2017/open-digger",
    metavar="<org>/<repo>",
)
@pass_environment
def repo(env: Environment, repos: t.List[t.Tuple[str, str]]):
    """
    Operate on repository indicators
    """
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("[bold green]fetching repos info..."):
            print_repo_info(repos, env.cli_config.github_pat)
    else:
        env.set_mode("repo")
        env.set_params(repos)


@click.group(
    chain=True,
    help="Query indicators",
    invoke_without_command=True,
)
@click.option(
    "--index",
    "-i",
    "index_flag",
    flag_value="index",
    help="Select indicators whose type is INDEX.",
    default=False,
    callback=add_indicator_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--metric",
    "-m",
    "metric_flag",
    flag_value="metric",
    help="Select indicators whose type is METRIC.",
    default=False,
    callback=add_indicator_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--network",
    "-n",
    "network_flag",
    flag_value="network",
    help="Select indicators whose type is NETWORK.",
    default=False,
    callback=add_indicator_type,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--x-lab",
    "-x",
    "x_lab_flag",
    flag_value="X-lab",
    help="Select indicators whose introducer is X-lab.",
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
    help="Select indicators whose introducer is CHAOSS.",
    default=False,
    callback=add_introducer,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--select",
    "-s",
    "selected_indicator_queries",
    type=FILTERED_METRIC_QUERY_TYPE,
    multiple=True,
    help="The indicator to select.",
    required=False,
)
@click.option(
    "--only-select/--no-only-select",
    "-o/-N",
    "is_only_select",
    is_flag=True,
    default=False,
    help="Only query selected indicators.",
)
@click.option(
    "--ignore",
    "-I",
    "ignore_indicator_names",
    multiple=True,
    type=IGNORED_METRIC_NAME_TYPE,
    help="The indicators to ignore.",
    required=False,
)
def query(
    indicator_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
    selected_indicator_queries: t.List[
        t.Tuple[str, t.Optional["IndicatorQuery"]]
    ],
    is_only_select: bool,
    ignore_indicator_names: t.List[str],
):
    """
    Query Metrics

    if you don't specify any options, all indicator name will be displayed
    if --all is set, all indicators will be queried
    """
    pass


query_cmd = t.cast("Group", query)


@query_cmd.result_callback()
# this is stored in Context's meta and assigned in the query option's callback
@pass_filtered_dataloaders
@pass_environment
def process_query_results(
    env: "Environment",
    filtered_dataloaders: t.Dict[str, "DataloaderProto"],
    processors: t.List[t.Callable],
    indicator_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
    selected_indicator_queries: t.List[
        t.Tuple[str, t.Optional["IndicatorQuery"]]
    ],
    is_only_select: bool,
    ignore_indicator_names: t.List[str],
):
    # Processing parameters: deduplication and default value processing
    selected_indicator_queries = distinct_indicator_queries(
        selected_indicator_queries
    )
    ignore_indicator_names = distinct_indicator_names(ignore_indicator_names)
    if not indicator_types and not introducers:
        indicator_types = {"index", "metric", "network"}
        introducers = {"X-lab", "CHAOSS"}

    env.vlog(
        f"""Parameters:
        indicator_types: {indicator_types},
        introducers: {introducers}, 
        selected_indicator_queries: {selected_indicator_queries}, 
        is_only_select: {is_only_select},
        ignore_indicator_names: {ignore_indicator_names}
        """
    )

    # If the subcommand is not called, then print the filtered indicators information
    if click.get_current_context().invoked_subcommand is None:
        with CONSOLE.status("Loading indicators info..."):
            print_indicator_info(
                mode=env.mode,
                indicator_types=t.cast(
                    t.Set[t.Literal["index", "metric", "network"]],
                    indicator_types,
                ),
                introducers=t.cast(
                    t.Set[t.Literal["X-lab", "CHAOSS"]], introducers
                ),
            )
            return

    # Query only selected indicators
    if is_only_select:
        if not selected_indicator_queries:
            raise click.UsageError(
                "You must specify the indicators you want to query."
            )
        env.vlog("Query only selected indicators")
        dataloaders = [
            filtered_dataloaders[indicator_name]
            for indicator_name, _ in selected_indicator_queries
        ]
    else:  # Query all indicators
        env.vlog("Query all indicators")
        dataloaders = list(filtered_dataloaders.values())

    mode = env.mode  # This is assigned in the repo command
    if mode == "user":
        usernames = t.cast(t.List[str], env.params)
        # build result
        results = [
            QueryUserResult(
                username=username,
                dataloaders=dataloaders,
                indicator_queries=selected_indicator_queries,
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
            indicator_queries=selected_indicator_queries,
        )
        for repo in repos
    ]

    env.vlog("Query Results:", results)

    # add result to context
    env.add_query_results(results)
    env.vlog(
        f"Save Query Results to Context Meta: {'[green]Success[/]' if env.get_query_results() is not None else '[red]Error[/]'}"
    )

    return process_commands(processors, results)


user.add_command(query_cmd)
repo.add_command(query_cmd)
