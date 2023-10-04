import typing as t
from pathlib import Path
import datetime

from opendigger_pycli.console import CONSOLE
from opendigger_pycli.console.print_indicator import (
    SURPPORTED_DISPLAY_FORMAT_TYPE,
    print_non_trivial_indicator,
    print_non_trivial_network_indciator,
    print_trivial_indicator,
    print_trivial_network_indicator,
)
from opendigger_pycli.datatypes import (
    NON_TRIVAL_NETWORK_INDICATOR_DATA,
    NON_TRIVIAL_INDICATOR_DATA,
    TRIVIAL_INDICATOR_DATA,
    TRIVIAL_NETWORK_INDICATOR_DATA,
)
from opendigger_pycli.results.query import RepoQueryResult, UserQueryResult

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.query import IndicatorQuery
    from opendigger_pycli.results.query import QueryResults


class DisplyCMDResult:
    query_results: "QueryResults"
    mode: SURPPORTED_DISPLAY_FORMAT_TYPE
    save_path: t.Optional[Path]

    def __init__(
        self,
        query_results: "QueryResults",
        mode: SURPPORTED_DISPLAY_FORMAT_TYPE,
        save_path: t.Optional[Path] = None,
        **kwargs,
    ) -> None:
        self.query_results = query_results
        self.mode = mode
        self.save_path = save_path

        self.paging = kwargs.get("paging", True)
        self.pager_color = kwargs.get("pager_color", True)

    def _handle_query_result(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> None:
        queried_indicators_data = query_result.queried_data
        failed_queries = query_result.failed_query
        for (
            indicator_name,
            indicator_dataloder_result,
        ) in queried_indicators_data.items():
            indicator_name_formated = indicator_name.replace("_", " ").title()
            if (
                not indicator_dataloder_result.is_success
                or not indicator_dataloder_result.data
            ):
                CONSOLE.print(
                    f"[red]Failed to load {indicator_name_formated} indicator data: {indicator_dataloder_result.desc}"
                )
                continue
            indicator_data_class = indicator_dataloder_result.data.data_class

            def _print_indicator_data(indicator_dataloder_result) -> None:
                if indicator_data_class == TRIVIAL_NETWORK_INDICATOR_DATA:
                    print_trivial_network_indicator(
                        indicator_name,
                        indicator_dataloder_result.data,
                        t.cast(
                            "t.Optional[IndicatorQuery]",
                            failed_queries[indicator_name],
                        ),
                        self.mode,
                    )
                elif indicator_data_class == NON_TRIVAL_NETWORK_INDICATOR_DATA:
                    print_non_trivial_network_indciator(
                        indicator_name,
                        indicator_dataloder_result.data,
                        t.cast(
                            "t.Optional[IndicatorQuery]",
                            failed_queries[indicator_name],
                        ),
                        self.mode,
                    )
                elif indicator_data_class == TRIVIAL_INDICATOR_DATA:
                    print_trivial_indicator(
                        indicator_name,
                        indicator_dataloder_result.data,
                        t.cast(
                            "t.Optional[IndicatorQuery]",
                            failed_queries[indicator_name],
                        ),
                        self.mode,
                    )
                elif indicator_data_class == NON_TRIVIAL_INDICATOR_DATA:
                    failed_queries[indicator_name]
                    print_non_trivial_indicator(
                        indicator_name,
                        indicator_dataloder_result.data,
                        t.cast(
                            "t.Dict[str, IndicatorQuery]",
                            failed_queries[indicator_name],
                        ),
                        self.mode,
                    )
                else:
                    raise ValueError(
                        f"Unknown indicator data class: {indicator_dataloder_result}"
                    )

            if self.paging:
                with CONSOLE.pager(styles=self.pager_color):
                    _print_indicator_data(indicator_dataloder_result)
            else:
                _print_indicator_data(indicator_dataloder_result)

    def _handle_title(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> None:
        if query_result.__class__ is RepoQueryResult:
            query_result = t.cast(RepoQueryResult, query_result)
            title = f"[green bold]Repo: {query_result.org_name}/{query_result.repo_name} Indicator Data"
        else:
            query_result = t.cast(UserQueryResult, query_result)
            title = f"[green bold]User: {query_result.username} Indicator Data"
        CONSOLE.print(title, justify="center")
        CONSOLE.print()

    def _handle_save_path(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> t.Optional[str]:
        if self.save_path is None:
            return None
        self.save_path.mkdir(parents=True, exist_ok=True)

        curr_datetime_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if query_result.__class__ is RepoQueryResult:
            query_result = t.cast(RepoQueryResult, query_result)
            save_path = str(
                self.save_path
                / f"repo-{query_result.org_name}#{query_result.repo_name}-{self.mode}-{curr_datetime_str}.html"
            )
        else:
            query_result = t.cast(UserQueryResult, query_result)
            save_path = str(
                self.save_path
                / f"user-{query_result.username}#{self.mode}-{curr_datetime_str}.html"
            )
        return save_path

    def display(self) -> None:
        if not self.query_results:
            CONSOLE.print("[red]No results to display")
            return

        if self.save_path is not None and self.paging:
            CONSOLE.print(
                "[yellow]You cannot use save output and paging at the same time, paging will be disabled"
            )
            self.paging = False

        save_paths = []
        for query_result in self.query_results:
            if not query_result.queried_data:
                continue

            if self.paging:
                with CONSOLE.pager(styles=self.pager_color):
                    self._handle_title(query_result)
            else:
                self._handle_title(query_result)

            self._handle_query_result(query_result)

            save_path = self._handle_save_path(query_result)
            if save_path is not None:
                save_paths.append(save_path)
                with open(save_path, "w") as f:
                    f.write(CONSOLE.export_html())

        for save_path in save_paths:
            CONSOLE.print(f"[green]Saving results to[/] {save_path}")
