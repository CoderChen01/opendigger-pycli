import typing as t

from opendigger_pycli.console import CONSOLE

if t.TYPE_CHECKING:
    from opendigger_pycli.results.query import QueryResults


def print_query_results_to_table(query_results: "QueryResults"):
    CONSOLE.print("call print_query_results_to_table")


def print_query_results_to_json(query_results: "QueryResults"):
    CONSOLE.print("call print_query_results_to_json")


def print_query_results_to_object(query_results: "QueryResults"):
    CONSOLE.print("call print_query_results_to_object")
