import typing as t

import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points  # type: ignore

from opendigger_pycli.console import CONSOLE
from opendigger_pycli.console.print_base_info import (
    print_indicator_info,
    print_repo_info,
    print_user_info,
)
from opendigger_pycli.results.query import RepoQueryResult, UserQueryResult
from opendigger_pycli.utils.decorators import (
    pass_filtered_dataloaders,
    process_commands,
)

from .custom_types import (
    FILTERED_METRIC_QUERY_TYPE,
    GH_REPO_NAME_TYPE,
    GH_USERNAME_TYPE,
    IGNORED_METRIC_NAME_TYPE,
    INDICATOR_QUERY_TYPE,
)
from .env import Environment
from .utils import (
    add_indicator_type,
    add_introducer,
    distinct_indicator_names,
    distinct_indicator_queries,
)

if t.TYPE_CHECKING:
    from click import Group

    from opendigger_pycli.datatypes import DataloaderProto, IndicatorQuery


pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group(  # type: ignore
    context_settings={
        "help_option_names": ["-h", "--help"],
    }
)
@click.option(
    "--log-level",
    "-L",
    "log_level",
    type=click.Choice(["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Enables verbose mode.",
)
@pass_environment
def opendigger(
    env: Environment,
    log_level: t.Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
) -> None:
    """Open Digger CLI"""
    env.set_log_level(log_level)


opendigger_cmd = t.cast("Group", opendigger)


@opendigger_cmd.group(invoke_without_command=True)  # type: ignore
@click.option(
    "--username",
    "-u",
    "usernames",
    type=GH_USERNAME_TYPE,
    multiple=True,
    help="GitHub username",
)
@pass_environment
def user(env: Environment, usernames: t.List[str]) -> None:
    """
    Operate on user indicators
    """
    env.vlog("indicator mode: [green]USER")

    usernames = list(set(usernames))
    env.dlog("usernames:", usernames)

    if click.get_current_context().invoked_subcommand is None:
        env.vlog("[bold green]requesting users info...")
        with CONSOLE.status("[bold green]requesting users info..."):
            env.dlog(print_user_info(usernames, env.cli_config.app_keys.github_pat))
            env.vlog("[bold green]end requesting users info...")
            return

    if not usernames:
        env.elog("You must specify the username.")
        raise click.UsageError("You must specify the username.")

    env.set_mode("user")
    env.set_params(usernames)
    env.dlog("Set params to env")
    env.dlog("env.mode:", env.mode)
    env.dlog("env.params:", env.params)


@opendigger_cmd.group(invoke_without_command=True)  # type: ignore
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
def repo(env: Environment, repos: t.List[t.Tuple[str, str]]) -> None:
    """
    Operate on repository indicators
    """
    env.vlog("indicator mode: [green]REPO")

    repos = list(set(repos))
    env.dlog("repos:", repos)

    if click.get_current_context().invoked_subcommand is None:
        env.vlog("[bold green]fetching repos info...")
        with CONSOLE.status("[bold green]fetching repos info..."):
            env.dlog(print_repo_info(repos, env.cli_config.app_keys.github_pat))
            env.vlog("[bold green]end fetching repos info...")
        return

    if not repos:
        env.elog("You must specify the repository.")
        raise click.UsageError("You must specify the repository.")

    env.set_mode("repo")
    env.set_params(repos)
    env.vlog("Set params to env")


@with_plugins(iter_entry_points("opendigger_pycli.plugins"))  # type: ignore
@click.group(  # type: ignore
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
@click.option(
    "--fileter",
    "-f",
    "uniform_query",
    type=INDICATOR_QUERY_TYPE,
    required=False,
    is_eager=True,
    help="The query applying to all indicators",
)
def query(
    indicator_types: t.Set[t.Literal["index", "metric", "network"]],
    introducers: t.Set[t.Literal["X-lab", "CHAOSS"]],
    selected_indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]],
    is_only_select: bool,
    ignore_indicator_names: t.List[str],
    uniform_query: t.Optional["IndicatorQuery"],
) -> None:
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
    selected_indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]],
    is_only_select: bool,
    ignore_indicator_names: t.List[str],
    uniform_query: t.Optional["IndicatorQuery"],
) -> None:
    # Processing parameters: deduplication and default value processing
    selected_indicator_queries = distinct_indicator_queries(selected_indicator_queries)
    ignore_indicator_names = distinct_indicator_names(ignore_indicator_names)
    if not indicator_types and not introducers:
        indicator_types = {"index", "metric", "network"}
        introducers = {"X-lab", "CHAOSS"}

    env.vlog("Start to query indicators...")
    env.dlog(
        f"""Parameters:
        indicator_types: {indicator_types},
        introducers: {introducers},
        selected_indicator_queries: {selected_indicator_queries},
        is_only_select: {is_only_select},
        ignore_indicator_names: {ignore_indicator_names},
        uniform_query: {uniform_query}
        """
    )

    # If the subcommand is not called,
    # then print the filtered indicators information
    if click.get_current_context().invoked_subcommand is None:
        env.vlog("Loading indicators info...")
        with CONSOLE.status("Loading indicators info..."):
            env.dlog(
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
            )
            env.vlog("End loading indicators info...")
            return

    # Query only selected indicators
    if is_only_select:
        env.vlog("Query only selected indicators")
        dataloaders = [
            filtered_dataloaders[indicator_name]
            for indicator_name, _ in selected_indicator_queries
            if indicator_name not in ignore_indicator_names
        ]
    else:  # Query all indicators
        env.vlog("Query all indicators")
        dataloaders = dataloaders = [
            filtered_dataloaders[indicator_name]
            for indicator_name in filtered_dataloaders
            if indicator_name not in ignore_indicator_names
        ]

    if not dataloaders:
        env.elog("Your query cannot query any indicators.")
        raise click.UsageError("Your query cannot query any indicators.")

    mode = env.mode  # This is assigned in the repo command
    results: t.Union[t.List[UserQueryResult], t.List[RepoQueryResult]]
    if mode == "user":
        usernames = t.cast(t.List[str], env.params)
        # build result
        env.vlog("Fetching user indicators data...")
        results = [
            UserQueryResult(
                username=username,
                dataloaders=dataloaders,
                indicator_queries=selected_indicator_queries,
                uniform_query=uniform_query,
            )
            for username in usernames
        ]
    else:
        # repo mode
        repos = t.cast(t.List[t.Tuple[str, str]], env.params)
        # build result
        env.vlog("Fetching repo indicators data...")
        results = [
            RepoQueryResult(
                repo=repo,
                dataloaders=dataloaders,
                indicator_queries=selected_indicator_queries,
                uniform_query=uniform_query,
            )
            for repo in repos
        ]

    env.vlog("End fetching indicators data...")
    env.dlog("Query Results:", results)

    return process_commands(processors, results)


user.add_command(query_cmd)
repo.add_command(query_cmd)
