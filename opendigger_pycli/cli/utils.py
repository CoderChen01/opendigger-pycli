import typing as t
from collections import defaultdict

import click

from opendigger_pycli.dataloaders import filter_dataloader

if t.TYPE_CHECKING:
    from click import Context

    from opendigger_pycli.datatypes import IndicatorQuery


def update_filtered_indicator_dataloaders(ctx: "Context") -> None:
    if "indicator_types" in ctx.params and ctx.params["indicator_types"]:
        indicator_types = ctx.params["indicator_types"]
    else:
        indicator_types = {"index", "metric", "network"}

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
            indicator_types,
        ),
        t.cast(t.Set[t.Literal["X-lab", "CHAOSS"]], introducers),
    )
    ctx.meta["filtered_dataloaders"] = {
        dataloader.name: dataloader for dataloader in dataloaders
    }


def add_indicator_type(
    ctx: click.Context,
    param: click.Parameter,
    value: t.Literal["index", "indicator", "network"],
) -> None:
    if "indicator_types" in ctx.params:
        if value is None:
            return
        if isinstance(ctx.params["indicator_types"], set):
            ctx.params["indicator_types"].add(value)
        else:
            ctx.params["indicator_types"] = set()
            ctx.params["indicator_types"].add(value)
    elif value is not None:
        ctx.params["indicator_types"] = set()
        ctx.params["indicator_types"].add(value)
    else:
        ctx.params["indicator_types"] = set()
    update_filtered_indicator_dataloaders(ctx)


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

    update_filtered_indicator_dataloaders(ctx)


def distinct_indicator_queries(
    indicator_quries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]
) -> t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]:
    indicator_query_dict = defaultdict(list)
    for indicator_query in indicator_quries:
        indicator_name, query = indicator_query
        indicator_query_dict[indicator_name].append(query)

    new_indicator_queries = []
    for indicator_name, queries in indicator_query_dict.items():
        queries_set = set(queries)
        for query in queries_set:
            new_indicator_queries.append((indicator_name, query))

    return new_indicator_queries


def distinct_indicator_names(indicator_names: t.List[str]) -> t.List[str]:
    return list(set(indicator_names))
