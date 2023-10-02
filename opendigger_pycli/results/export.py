import datetime
import json
import typing as t

from opendigger_pycli.console import CONSOLE
from opendigger_pycli.console.utils import print_failed_query
from opendigger_pycli.exporters import JSON_FORMT, REPORT_FORMAT
from opendigger_pycli.exporters.chart_exporter import ChartReportExporter
from opendigger_pycli.exporters.json_exporter import export_indicator_to_json

from .query import QueryResults, RepoQueryResult, UserQueryResult

if t.TYPE_CHECKING:
    from pathlib import Path

    from opendigger_pycli.exporters import (
        SURPPORTED_EXPORT_FORMAT_TYPE,
        SURPPORTED_EXPORT_FORMATS,
    )


class ExportResult:
    query_results: "QueryResults"
    format: "SURPPORTED_EXPORT_FORMAT_TYPE"
    save_path: "Path"
    is_split: bool

    def __init__(
        self,
        query_results: "QueryResults",
        format: "SURPPORTED_EXPORT_FORMAT_TYPE",
        save_path: "Path",
        is_split: bool,
        **kwargs,
    ) -> None:
        self.query_results = query_results
        self.format = format
        self.save_path = save_path
        self.is_split = is_split

    def _query_result_to_json(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> t.Dict[str, t.Dict]:
        result: t.Dict[str, t.Dict] = {}
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

            failed_query = failed_queries.get(indicator_name)
            if failed_query:
                if isinstance(failed_query, dict):
                    for key, value in failed_query.items():
                        if value is not None:
                            continue
                        print_failed_query(indicator_name + "." + key, value)
                else:
                    print_failed_query(indicator_name, failed_query)

            result[indicator_name] = export_indicator_to_json(
                indicator_dataloder_result.data
            )

        return result

    def _query_result_to_report(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> str:
        chart_report_exporter = ChartReportExporter()

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

            failed_query = failed_queries.get(indicator_name)
            if failed_query:
                if isinstance(failed_query, dict):
                    for key, value in failed_query.items():
                        if value is not None:
                            continue
                        print_failed_query(indicator_name + "." + key, value)
                else:
                    print_failed_query(indicator_name, failed_query)

            chart_report_exporter.add_indicator_data(indicator_dataloder_result.data)

        if query_result.__class__ is RepoQueryResult:
            query_result = t.cast(RepoQueryResult, query_result)
            title = f"Repo {query_result.org_name}/{query_result.repo_name} Indicator Report"
        else:
            query_result = t.cast(UserQueryResult, query_result)
            title = f"User {query_result.username} Indicator Report"

        return chart_report_exporter.export(title)

    def _handle_save_path(
        self, query_result: t.Union["RepoQueryResult", "UserQueryResult"]
    ) -> t.Optional["Path"]:
        if self.save_path is None:
            return None

        self.save_path.mkdir(parents=True, exist_ok=True)

        current_datetime_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if query_result.__class__ is RepoQueryResult:
            query_result = t.cast(RepoQueryResult, query_result)
            base_path = (
                self.save_path
                / f"repo-{query_result.org_name}-{query_result.repo_name}"
            )
        else:
            query_result = t.cast(UserQueryResult, query_result)
            base_path = self.save_path / f"user-{query_result.username}"

        if self.is_split:
            save_path = base_path / self.format / current_datetime_str
            save_path.mkdir(parents=True, exist_ok=True)
        else:
            base_path.mkdir(parents=True, exist_ok=True)
            if self.format == JSON_FORMT:
                save_path = (base_path / current_datetime_str).with_suffix(".json")
            elif self.format == REPORT_FORMAT:
                save_path = (base_path / current_datetime_str).with_suffix(".html")
            else:
                raise ValueError(f"Unknown format {self.format}")

        return save_path

    def export(self) -> None:
        if not self.query_results:
            CONSOLE.print("[red]No results to export")
            return

        for query_result in self.query_results:
            save_path = self._handle_save_path(query_result)
            if save_path is None:
                raise ValueError("Save path is None")

            if self.format == "json":
                result = self._query_result_to_json(query_result)

                if self.is_split:
                    for indicator_name, indicator_json_data in result.items():
                        save_path_splited = save_path / f"{indicator_name}.json"
                        save_path_splited.write_text(
                            json.dumps(indicator_json_data, indent=2, sort_keys=True)
                        )
                        CONSOLE.print(
                            f"[green]Save Indicator {indicator_name} Data to {save_path}"
                        )
                else:
                    save_path.write_text(json.dumps(result, indent=2, sort_keys=True))
                    CONSOLE.print(f"[green]Save All Indicator Data to {save_path}")
            else:
                rv = self._query_result_to_report(query_result)
                save_path.write_text(rv, encoding="utf-8")
                CONSOLE.print(f"[green]Save Report to {save_path}")
