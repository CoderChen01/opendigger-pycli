import abc
import base64
import math
import typing as t
from collections import OrderedDict
from dataclasses import asdict
from functools import cached_property
from pathlib import Path

import urllib3
from jinja2 import Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts import types
from pyecharts.charts import Bar, Candlestick, Graph, HeatMap, Line, Tab, Timeline
from pyecharts.charts.base import Base
from pyecharts.commons.utils import JsCode
from pyecharts.options import InitOpts, RenderOpts
from pyecharts.types import Optional, Union

from opendigger_pycli.datatypes import (
    AcceptedChangeRequestData,
    ActiveDateAndTimeData,
    ActivityData,
    ActivityDetailData,
    AddedCodeChangeLineData,
    AttentionData,
    BusFactorData,
    ChangeRequestAgeData,
    ChangeRequestData,
    ChangeRequestResolutionDurationData,
    ChangeRequestResponseTimeData,
    ChangeRequestReviewData,
    ClosedIssueData,
    DeveloperNetworkData,
    InactiveContributorData,
    IssueAgeData,
    IssueCommentData,
    IssueResolutionDurationData,
    IssueResponseTimeData,
    NewContributorData,
    NewIssueData,
    OpenRankData,
    ParticipantData,
    ProjectOpenRankNetworkData,
    RemovedCodeChangeLineData,
    RepoNetworkData,
    StarData,
    SumCodeChangeLineData,
    TechnicalForkData,
)

from .ai_report_utils import analyze_indicators_data

if t.TYPE_CHECKING:
    from pyecharts.charts.base import Base as EchartsBase

JINJA_ENV = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent / "templates"))
)


class ChartReportExporter:
    exporters: t.Dict[str, "BaseChartExporter"] = {}
    custom_exporters: t.Dict[str, "BaseChartExporter"] = {}

    def register_custom_exporter(self, exporter: t.Type["BaseChartExporter"]) -> None:
        ChartReportExporter.custom_exporters[exporter.exporter_name] = exporter()

    def add_indicator_data(self, indicator_data: t.Any) -> None:
        is_added = False
        for exporter_name, exporter in ChartReportExporter.exporters.items():
            if exporter_name in ChartReportExporter.custom_exporters:
                exporter = ChartReportExporter.custom_exporters[exporter_name]
            if indicator_data.__class__ in exporter.accepted_indicator_dataclass:
                exporter.add_indicator_data(indicator_data)
                is_added = True
        if not is_added:
            raise ValueError(
                f"Indicator {indicator_data.__class__.name} is not accepted by any exporter"
            )

    def get_all_export_datum(self) -> t.List["ExportData"]:
        export_datum = []
        for exporter_name, exporter in ChartReportExporter.exporters.items():
            if exporter_name in ChartReportExporter.custom_exporters:
                exporter = ChartReportExporter.custom_exporters[exporter_name]
            export_datum.extend(exporter.get_export_datum())
        return export_datum

    def export(self, title: str) -> str:
        jinja_env = JINJA_ENV
        tab_chart = Tab(title)

        export_extra_data = {}
        for export_data in self.get_all_export_datum():
            tab_chart.add(export_data.chart, export_data.name)
            export_extra_data[export_data.chart.chart_id] = (
                export_data.extra_data if export_data.extra_data else {}
            )

        return tab_chart.render_embed(
            template_name="report.html",
            env=jinja_env,
            extra_chart_datum=export_extra_data,
        )


def register_exporter(exporter: t.Type["BaseChartExporter"]) -> None:
    ChartReportExporter.exporters[exporter.exporter_name] = exporter()


def get_indicator_title(indicator_name: str) -> str:
    return indicator_name.replace("_detail", "").replace("_", " ").title()


class ExportData(t.NamedTuple):
    name: str
    chart: "EchartsBase"
    extra_data: t.Optional[t.Dict[str, t.Union[str, int, float, bool]]] = None


class BaseChartExporter(abc.ABC):
    exporter_name: t.ClassVar[str]
    accepted_indicator_dataclass: t.ClassVar[t.List[t.Type]]

    def __init__(self) -> None:
        self.indicator_datum: t.List[t.Any] = []

    def add_indicator_data(self, indicator_data: t.Any) -> None:
        if indicator_data.__class__ not in self.accepted_indicator_dataclass:
            raise ValueError(
                f"Indicator {indicator_data.__class__.name} is not accepted by {self.exporter_name}"
            )
        self.indicator_datum.append(indicator_data)

    def get_export_datum(self) -> t.List[ExportData]:
        export_datum = self.export()
        if hasattr(self, "post_process") and callable(getattr(self, "post_process")):
            getattr(self, "post_process")(export_datum)
        return export_datum

    @abc.abstractmethod
    def export(self) -> t.List[ExportData]:
        pass


@register_exporter
class BarExporter(BaseChartExporter):
    exporter_name = "bar_exporter"
    accepted_indicator_dataclass = [OpenRankData, ActivityData]

    def export(self) -> t.List[ExportData]:
        export_datum = []
        for indicator_data in self.indicator_datum:
            bar = Bar()
            x_axis_data = []
            y_axis_data = []
            for base_data in indicator_data.value:
                x_axis_data.append(f"{base_data.year}-{base_data.month:02}")
                y_axis_data.append(base_data.value)

            (
                bar.add_xaxis(x_axis_data)
                .add_yaxis(
                    "openrank", y_axis_data, label_opts=opts.LabelOpts(is_show=False)
                )
                .set_global_opts(
                    legend_opts=opts.LegendOpts(is_show=False),
                )
            )
            ai_rv = analyze_indicators_data([indicator_data])
            export_datum.append(
                ExportData(name=indicator_data.name, chart=bar, extra_data=ai_rv)  # type: ignore
            )
        return export_datum


@register_exporter
class SumAndDetailExporter(BaseChartExporter):
    exporter_name = "sum_and_detail_exporter"
    accepted_indicator_dataclass = [ActivityDetailData, BusFactorData]

    def __handle_bar_detail_chart(
        self, indicator_data: t.Any
    ) -> t.Tuple["EchartsBase", "EchartsBase"]:
        indicator_name = get_indicator_title(indicator_data.name)
        bar_sum = Bar()

        x_axis_data = []
        y_axis_data_sum = []
        y_axis_data_detail = []
        for base_data in indicator_data.value:
            x_axis_data.append(f"{base_data.year}-{base_data.month:02}")
            y_axis_data_sum.append(round(sum((v.value for v in base_data.value)), 2))
            y_axis_data_detail.append([v.tuple for v in base_data.value])
        bar_sum.add_xaxis(x_axis_data).add_yaxis(
            f"{indicator_name} Sum",
            y_axis_data_sum,
            label_opts=opts.LabelOpts(is_show=False),
        ).set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
        )

        time_line = Timeline()
        for idx, x in enumerate(x_axis_data):
            c_data = y_axis_data_detail[idx]
            values = [v[1] for v in c_data]
            min_v = t.cast(float, min(values))
            max_v = t.cast(float, max(values))
            bar = (
                Bar()
                .add_dataset(source=c_data, source_header=False)
                .add_yaxis(
                    series_name="",
                    encode={"x": 1, "y": 0},
                    y_axis=[],
                    label_opts=opts.LabelOpts(
                        position="right",
                    ),
                    is_realtime_sort=True,
                )
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(
                        max_="dataMax",
                        axislabel_opts=opts.LabelOpts(
                            formatter=JsCode(
                                """function (n) {
                                    return Math.round(n) + '';
                                }"""
                            ),
                        ),
                    ),
                    yaxis_opts=opts.AxisOpts(
                        type_="category",
                        is_inverse=True,
                        max_=10,
                        splitline_opts=opts.SplitLineOpts(is_show=False),
                        axislabel_opts=opts.LabelOpts(
                            is_show=True,
                            font_size=14,
                            formatter=JsCode(
                                """function (value) {
                                    if (!value || value.endsWith('[bot]')) return value;
                                    return `${value} {avatar${value.replaceAll('-', '')}|}`;
                                }"""
                            ),
                            rich={
                                f"avatar{data[0].replace('-', '')}": {
                                    "backgroundColor": {
                                        "image": f"https://avatars.githubusercontent.com/{data[0]}?s=48&v=4"
                                    },
                                    "height": 20,
                                }
                                for data in c_data
                            },
                        ),
                    ),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=False,
                        min_=min_v,
                        max_=max_v,
                        dimension=1,
                        range_color=["#D7DA8B", "#E15457"],
                    ),
                    graphic_opts=[
                        opts.GraphicText(
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                text=x,
                                font="bolder 60px monospace",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="rgba(100, 100, 100, 0.25)"
                                ),
                            ),
                            graphic_item=opts.GraphicItem(z=100, right=60, bottom=60),
                        )
                    ],
                )
            )
            time_line.add(bar, x)

        return bar_sum, time_line

    def export(self) -> t.List[ExportData]:
        export_datum = []
        for indicator_data in self.indicator_datum:
            indicator_name = get_indicator_title(indicator_data.name)
            activity_sum, activity_detail = self.__handle_bar_detail_chart(
                indicator_data
            )
            export_datum.append(
                ExportData(
                    name=f"{indicator_name} Sum",
                    chart=activity_sum,
                )
            )
            export_datum.append(
                ExportData(name=f"{indicator_name} Details", chart=activity_detail, extra_data=analyze_indicators_data([indicator_data]))  # type: ignore
            )
        return export_datum


@register_exporter
class AccumulatedBarExporter(BaseChartExporter):
    exporter_name = "accumulated_bar_exporter"
    accepted_indicator_dataclass = [
        AttentionData,
        StarData,
        TechnicalForkData,
    ]

    def export(self) -> t.List[ExportData]:
        export_datum = []

        for indicator_data in self.indicator_datum:
            bar = Bar()
            line = Line()

            x_axis_data = []
            y_axis_data = []
            y_acc_axis_data = []
            for base_data in indicator_data.value:
                x_axis_data.append(f"{base_data.year}-{base_data.month:02}")
                y_axis_data.append(base_data.value)
                y_acc_axis_data.append(sum(y_axis_data))

            bar.add_xaxis(x_axis_data).add_yaxis(
                indicator_data.name.replace("_detail", ""),
                y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
            ).extend_axis(
                yaxis=opts.AxisOpts(name="Accumulated Value")
            ).set_series_opts(
                label_opts=opts.LabelOpts(is_show=False)
            ).set_global_opts(
                yaxis_opts=opts.AxisOpts(name=indicator_data.name)
            )

            line.add_xaxis(x_axis_data).add_yaxis(
                "Accumulated Value",
                y_acc_axis_data,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
                z_level=300,
            )
            bar.overlap(line)

            export_datum.append(
                ExportData(
                    name=indicator_data.name.replace("_detail", "")
                    .replace("_", " ")
                    .title(),
                    chart=bar,
                    extra_data=analyze_indicators_data([indicator_data]),  # type: ignore
                )
            )

        return export_datum


@register_exporter
class IssueStatusExporter(BaseChartExporter):
    exporter_name = "issue_status_exporter"
    accepted_indicator_dataclass = [NewIssueData, ClosedIssueData, IssueCommentData]

    def __get_new_and_closed_data(self):
        new_axis_data = OrderedDict()
        closed_axis_data = OrderedDict()

        new_indicator_data = None
        closed_indicator_data = None
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is NewIssueData:
                new_indicator_data = indicator_data
            elif indicator_data.__class__ is ClosedIssueData:
                closed_indicator_data = indicator_data
            else:
                continue

        if new_indicator_data is None and closed_indicator_data is None:
            return [], [], [], []

        if new_indicator_data is not None:
            for base_data in new_indicator_data.value:
                if base_data.is_raw:
                    continue
                new_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value

        if closed_indicator_data is not None:
            for base_data in closed_indicator_data.value:
                if base_data.is_raw:
                    continue
                closed_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value

        if len(new_axis_data) > len(closed_axis_data):
            monthes = list(new_axis_data.keys())
        else:
            monthes = list(closed_axis_data.keys())

        new_x = []
        new_y = []
        closed_x = []
        closed_y = []
        for month in monthes:
            new_x.append(month)
            new_y.append(new_axis_data.get(month, 0))
            closed_x.append(month)
            closed_y.append(closed_axis_data.get(month, 0))

        if new_indicator_data is None:
            new_x = []
            new_y = []

        if closed_indicator_data is None:
            closed_x = []
            closed_y = []

        return new_x, new_y, closed_x, closed_y

    def __handle_new_and_closed_issue_chart(self) -> t.Optional["Bar"]:
        bar = Bar()
        (
            new_x_axis_data,
            new_y_axis_data,
            closed_x_axis_data,
            closed_y_axis_data,
        ) = self.__get_new_and_closed_data()

        has_new_issue = len(new_x_axis_data) > 0
        has_closed_issue = len(closed_x_axis_data) > 0

        if not has_new_issue and not has_closed_issue:
            return None

        if has_new_issue and has_closed_issue:
            bar.add_xaxis(xaxis_data=new_x_axis_data)
            new_base_y_axis_data = [0]
            for i in range(1, len(new_y_axis_data)):
                new_base_y_axis_data.append(
                    new_y_axis_data[i - 1]
                    - closed_y_axis_data[i - 1]
                    + new_base_y_axis_data[i - 1]
                )
            closed_base_y_axis_data = []
            for i in range(len(new_y_axis_data)):
                closed_base_y_axis_data.append(
                    new_base_y_axis_data[i] + new_y_axis_data[i] - closed_y_axis_data[i]
                )

            bar.add_yaxis(
                "",
                new_base_y_axis_data,
                stack="Total",
                itemstyle_opts=opts.ItemStyleOpts(
                    color="transparent", border_color="transparent"
                ),
                color="transparent",
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(is_silent=True),
            ).add_yaxis(
                "",
                closed_base_y_axis_data,
                stack="CloseTotal",
                itemstyle_opts=opts.ItemStyleOpts(
                    color="transparent", border_color="transparent"
                ),
                label_opts=opts.LabelOpts(is_show=False),
                color="transparent",
                markline_opts=opts.MarkLineOpts(is_silent=True),
            )

        if has_new_issue:
            bar.add_xaxis(xaxis_data=new_x_axis_data)
            bar.add_yaxis(
                "New Issue",
                new_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="green"),
                stack="Total",
            )
        if has_closed_issue:
            bar.add_xaxis(xaxis_data=closed_x_axis_data)
            bar.add_yaxis(
                "Closed Issue",
                closed_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="red"),
                stack="CloseTotal",
            )

        bar.extend_axis(yaxis=opts.AxisOpts(name=""))
        bar.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True),
        )

        return bar

    def __handle_issue_comment_chart(self, yaxis_index: int = 1) -> t.Optional["Line"]:
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is not IssueCommentData:
                continue

            line = Line()
            x_axis_data = []
            y_axis_data = []
            for base_data in indicator_data.value:
                x_axis_data.append(f"{base_data.year}-{base_data.month:02}")
                y_axis_data.append(base_data.value)

            line.add_xaxis(xaxis_data=x_axis_data).add_yaxis(
                "Issue Comment",
                y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="blue"),
                z_level=300,
                yaxis_index=yaxis_index,
            )
            return line
        return None

    def export(self) -> t.List[ExportData]:
        bar = self.__handle_new_and_closed_issue_chart()

        if bar is not None:
            line = self.__handle_issue_comment_chart()
            if line is not None:
                bar.overlap(line)
            return [ExportData(name="Issue Status", chart=bar, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore
        else:
            line = self.__handle_issue_comment_chart(yaxis_index=0)
            if line is not None:
                return [ExportData(name="Issue Status", chart=line, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore

        return []


@register_exporter
class ChangeRequestStatusExporter(BaseChartExporter):
    exporter_name = "change_request_status_export"
    accepted_indicator_dataclass = [
        ChangeRequestData,
        ChangeRequestReviewData,
        AcceptedChangeRequestData,
    ]

    def __get_new_and_accepted_data(self):
        new_axis_data = OrderedDict()
        accepted_axis_data = OrderedDict()

        new_indicator_data = None
        accepted_indicator_data = None
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is ChangeRequestData:
                new_indicator_data = indicator_data
            elif indicator_data.__class__ is AcceptedChangeRequestData:
                accepted_indicator_data = indicator_data
            else:
                continue

        if new_indicator_data is None and accepted_indicator_data is None:
            return [], [], [], []

        if new_indicator_data is not None:
            for base_data in new_indicator_data.value:
                if base_data.is_raw:
                    continue
                new_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value

        if accepted_indicator_data is not None:
            for base_data in accepted_indicator_data.value:
                if base_data.is_raw:
                    continue
                accepted_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value

        if len(new_axis_data) > len(accepted_axis_data):
            monthes = list(new_axis_data.keys())
        else:
            monthes = list(accepted_axis_data.keys())

        new_x = []
        new_y = []
        accepted_x = []
        accepted_y = []
        for month in monthes:
            new_x.append(month)
            new_y.append(new_axis_data.get(month, 0))
            accepted_x.append(month)
            accepted_y.append(accepted_axis_data.get(month, 0))

        if new_indicator_data is None:
            new_x = []
            new_y = []

        if accepted_indicator_data is None:
            accepted_x = []
            accepted_y = []

        return new_x, new_y, accepted_x, accepted_y

    def __handle_new_and_closed_pr_chart(self) -> t.Optional["Bar"]:
        bar = Bar()
        (
            new_x_axis_data,
            new_y_axis_data,
            accepted_x_axis_data,
            accepted_y_axis_data,
        ) = self.__get_new_and_accepted_data()

        has_new_pr = len(new_x_axis_data) > 0
        has_accepted_pr = len(accepted_x_axis_data) > 0

        if not has_new_pr and not has_accepted_pr:
            return None

        if has_new_pr and has_accepted_pr:
            new_base_y_axis_data = [0]
            for i in range(1, len(new_y_axis_data)):
                new_base_y_axis_data.append(
                    new_y_axis_data[i - 1]
                    - accepted_y_axis_data[i - 1]
                    + new_base_y_axis_data[i - 1]
                )
            accepted_base_y_axis_data = []
            for i in range(len(new_y_axis_data)):
                accepted_base_y_axis_data.append(
                    new_base_y_axis_data[i]
                    + new_y_axis_data[i]
                    - accepted_y_axis_data[i]
                )

            bar.add_yaxis(
                "",
                new_base_y_axis_data,
                stack="Total",
                itemstyle_opts=opts.ItemStyleOpts(
                    color="transparent", border_color="transparent"
                ),
                color="transparent",
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(is_silent=True),
            ).add_yaxis(
                "",
                accepted_base_y_axis_data,
                stack="AcceptedTotal",
                itemstyle_opts=opts.ItemStyleOpts(
                    color="transparent", border_color="transparent"
                ),
                label_opts=opts.LabelOpts(is_show=False),
                color="transparent",
                markline_opts=opts.MarkLineOpts(is_silent=True),
            )

        if has_new_pr:
            bar.add_xaxis(xaxis_data=new_x_axis_data)
            bar.add_yaxis(
                "New Change Requests",
                new_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="green"),
                stack="Total",
            )
        if has_accepted_pr:
            bar.add_xaxis(xaxis_data=new_x_axis_data)
            bar.add_yaxis(
                "Accepted Change Requests",
                accepted_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="red"),
                stack="AcceptedTotal",
            )

        bar.extend_axis(yaxis=opts.AxisOpts(name=""))
        bar.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True),
        )

        return bar

    def __handle_change_request_review_chart(
        self, yaxis_index: int = 1
    ) -> t.Optional["Line"]:
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is not ChangeRequestReviewData:
                continue

            line = Line()
            x_axis_data = []
            y_axis_data = []
            for base_data in indicator_data.value:
                x_axis_data.append(f"{base_data.year}-{base_data.month:02}")
                y_axis_data.append(base_data.value)

            line.add_xaxis(xaxis_data=x_axis_data).add_yaxis(
                "Change Request Review",
                y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="blue"),
                z_level=300,
                yaxis_index=yaxis_index,
            )
            return line
        return None

    def export(self) -> t.List[ExportData]:
        bar = self.__handle_new_and_closed_pr_chart()

        if bar is not None:
            line = self.__handle_change_request_review_chart()
            if line is not None:
                bar.overlap(line)
            return [ExportData(name="Change Request Status", chart=bar, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore
        else:
            line = self.__handle_change_request_review_chart(yaxis_index=0)
            if line is not None:
                return [ExportData(name="Change Request Status", chart=line, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore

        return []


@register_exporter
class DeveloperStatusExporter(BaseChartExporter):
    exporter_name = "developer_status_exporter"
    accepted_indicator_dataclass = [
        ParticipantData,
        NewContributorData,
        InactiveContributorData,
    ]

    @cached_property
    def __all_data(self):
        new_axis_data = OrderedDict()
        inactive_axis_data = OrderedDict()
        participant_axis_data = OrderedDict()

        new_indicator_data = None
        inactive_indicator_data = None
        participan_indicator_data = None
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is NewContributorData:
                new_indicator_data = indicator_data
            elif indicator_data.__class__ is InactiveContributorData:
                inactive_indicator_data = indicator_data
            elif indicator_data.__class__ is ParticipantData:
                participan_indicator_data = indicator_data
            else:
                continue

        if new_indicator_data is None and inactive_indicator_data is None:
            return [], [], [], [], [], []

        monthes = []
        if new_indicator_data is not None:
            for base_data in new_indicator_data.value:
                if base_data.is_raw:
                    continue
                new_axis_data[f"{base_data.year}-{base_data.month:02}"] = len(
                    base_data.value
                )
            c_monthes = list(new_axis_data.keys())
            if len(c_monthes) > len(monthes):
                monthes = c_monthes

        if inactive_indicator_data is not None:
            for base_data in inactive_indicator_data.value:
                if base_data.is_raw:
                    continue
                inactive_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = -base_data.value
            c_monthes = list(inactive_axis_data.keys())
            if len(c_monthes) > len(monthes):
                monthes = c_monthes

        if participan_indicator_data is not None:
            for base_data in participan_indicator_data.value:
                if base_data.is_raw:
                    continue
                participant_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value
            c_monthes = list(participant_axis_data.keys())
            if len(c_monthes) > len(monthes):
                monthes = c_monthes

        new_x = []
        new_y = []
        inactive_x = []
        inactive_y = []
        participant_x = []
        participant_y = []
        for month in monthes:
            new_x.append(month)
            new_y.append(new_axis_data.get(month, 0))
            inactive_x.append(month)
            inactive_y.append(inactive_axis_data.get(month, 0))
            participant_x.append(month)
            participant_y.append(participant_axis_data.get(month, 0))

        if new_indicator_data is None:
            new_x = []
            new_y = []

        if inactive_indicator_data is None:
            inactive_x = []
            inactive_y = []

        if participan_indicator_data is None:
            participant_x = []
            participant_y = []

        return new_x, new_y, inactive_x, inactive_y, participant_x, participant_y

    def __handle_new_and_inactive_contrib_chart(self) -> t.Optional["Bar"]:
        bar = Bar()
        (
            new_x_axis_data,
            new_y_axis_data,
            inactive_x_axis_data,
            inactive_y_axis_data,
            _,
            _,
        ) = self.__all_data

        has_new_contrib = len(new_x_axis_data) > 0
        has_inactive_contrib = len(inactive_x_axis_data) > 0

        if not has_new_contrib and not has_inactive_contrib:
            return None

        has_x = False
        if has_new_contrib:
            if not has_x:
                bar.add_xaxis(xaxis_data=new_x_axis_data)
                has_x = True
            bar.add_yaxis(
                "New Contributors",
                new_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="green"),
            )
        if has_inactive_contrib:
            if not has_x:
                bar.add_xaxis(xaxis_data=inactive_x_axis_data)
                has_x = True
            bar.add_yaxis(
                "Inactive Contributors",
                inactive_y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="red"),
            )

        bar.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True),
        )

        return bar

    def __handle_participant_chart(self) -> t.Optional["Line"]:
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is not ParticipantData:
                continue

            line = Line()
            (
                _,
                _,
                _,
                _,
                x_axis_data,
                y_axis_data,
            ) = self.__all_data

            line.add_xaxis(x_axis_data).add_yaxis(
                "Participants",
                y_axis_data,
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color="blue"),
                z_level=300,
            )
            return line
        return None

    def export(self) -> t.List[ExportData]:
        line = self.__handle_participant_chart()

        if line is not None:
            bar = self.__handle_new_and_inactive_contrib_chart()
            if bar is not None:
                line.overlap(bar)
            return [
                ExportData(
                    name="Developer Status",
                    chart=line,
                    extra_data=analyze_indicators_data(self.indicator_datum),  # type: ignore
                )
            ]
        else:
            bar = self.__handle_new_and_inactive_contrib_chart()
            if bar is not None:
                return [ExportData(name="Developer Status", chart=bar, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore

        return []


@register_exporter
class ActiveDateAndTimeHeatmapExporter(BaseChartExporter):
    exporter_name = "active_date_and_time_heatmap_exporter"
    accepted_indicator_dataclass = [ActiveDateAndTimeData]

    @cached_property
    def __active_date_and_time_heatmap_data(self) -> t.Optional[t.List[t.List[int]]]:
        adt_data = None
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is ActiveDateAndTimeData:
                adt_data = indicator_data
                break
        if adt_data is None:
            return None

        # Sum up all the working hours
        values: t.List[int] = []
        for base_dat in adt_data.value:
            value = base_dat.value
            if len(values) == 0:
                values = value
            else:
                values = [v1 + v2 for v1, v2 in zip(values, value)]

        # Use log to smooth the data (comment this line if you want to use linear data)
        # values = [math.log(v + 1) for v in values]

        # Normalize to 0 - 10
        max_value = max(values)
        values = [math.ceil(v * 10 / max_value) for v in values]

        input_data = []
        for d in range(7):
            for h in range(24):
                index = d * 24 + h
                if index < len(values):
                    input_data.append([h, 6 - d, values[index]])
                else:
                    input_data.append([h, 6 - d, "-"])  # type: ignore

        return input_data

    def export(self) -> t.List[ExportData]:
        heatmap_data = self.__active_date_and_time_heatmap_data

        if heatmap_data is None:
            return []

        heatmap = (
            HeatMap()
            .add_xaxis(
                [
                    "12a",
                    "1a",
                    "2a",
                    "3a",
                    "4a",
                    "5a",
                    "6a",
                    "7a",
                    "8a",
                    "9a",
                    "10a",
                    "11a",
                    "12p",
                    "1p",
                    "2p",
                    "3p",
                    "4p",
                    "5p",
                    "6p",
                    "7p",
                    "8p",
                    "9p",
                    "10p",
                    "11p",
                ]
            )
            .add_yaxis(
                series_name="",
                yaxis_data=["Sun.", "Sat.", "Fri.", "Thu.", "Wed.", "Tue.", "Mon."],  # type: ignore
                value=heatmap_data,  # type: ignore
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    min_=0,
                    max_=10,
                    is_calculable=True,
                    orient="horizontal",
                    pos_left="center",
                ),
                yaxis_opts=opts.AxisOpts(
                    splitarea_opts=opts.SplitAreaOpts(is_show=True)
                ),
                xaxis_opts=opts.AxisOpts(
                    splitarea_opts=opts.SplitAreaOpts(is_show=True)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
            )
        )

        return [ExportData(name="Active Dates And Times", chart=heatmap, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore


@register_exporter
class TimeDurationRelatedExporter(BaseChartExporter):
    exporter_name = "time_duration_related_exporter"
    accepted_indicator_dataclass = [
        IssueAgeData,
        IssueResolutionDurationData,
        IssueResponseTimeData,
        ChangeRequestAgeData,
        ChangeRequestResolutionDurationData,
        ChangeRequestResponseTimeData,
    ]

    def export(self) -> t.List[ExportData]:
        export_datum = []

        for indicator_data in self.indicator_datum:
            monthes = []
            avg_y_axis_data = []

            avg_data = indicator_data.value["avg"]
            for avg in avg_data:
                monthes.append(f"{avg.year}-{avg.month:02}")
                avg_y_axis_data.append(avg.value)

            quantile_axis_data = []
            for quantile_idx in [1, 3, 0, 4]:
                d = []
                for i, quantile_dat in enumerate(
                    indicator_data.value[f"quantile{quantile_idx}"]
                ):
                    month_str = f"{quantile_dat.year}-{quantile_dat.month:02}"
                    if month_str != monthes[i]:
                        continue
                    d.append(quantile_dat.value)
                quantile_axis_data.append(d)
            quantile_axis_data = list(zip(*quantile_axis_data))

            candle_stick = (
                Candlestick()
                .add_xaxis(monthes)
                .add_yaxis(
                    "quantiles bot plot",
                    quantile_axis_data,
                    itemstyle_opts=opts.ItemStyleOpts(
                        color="rgba(0,0,180,0.4)",
                        color0="rgba(0,0,180,0.4)",
                        border_color="rgba(0,0,180,0.4)",
                        border_color0="rgba(0,0,180,0.4)",
                    ),
                )
            ).overlap(
                Line()
                .add_xaxis(monthes)
                .add_yaxis(
                    "average", avg_y_axis_data, is_smooth=True, is_symbol_show=False
                )
            )
            export_datum.append(
                ExportData(
                    indicator_data.name.replace("_detail", "")
                    .replace("_", " ")
                    .title(),
                    candle_stick,
                    extra_data=analyze_indicators_data([indicator_data]),  # type: ignore
                )
            )
        return export_datum


@register_exporter
class CodeChangeLinesExporter(BaseChartExporter):
    exporter_name = "code_change_lines_exporter"
    accepted_indicator_dataclass = [
        AddedCodeChangeLineData,
        RemovedCodeChangeLineData,
        SumCodeChangeLineData,
    ]

    @cached_property
    def __all_data(self):
        add_axis_data = OrderedDict()
        remove_axis_data = OrderedDict()

        add_indicator_data = None
        remove_indicator_data = None
        for indicator_data in self.indicator_datum:
            if indicator_data.__class__ is AddedCodeChangeLineData:
                add_indicator_data = indicator_data
            elif indicator_data.__class__ is RemovedCodeChangeLineData:
                remove_indicator_data = indicator_data
            else:
                continue

        if add_indicator_data is None and remove_indicator_data is None:
            return [], [], [], []

        if add_indicator_data is not None:
            for base_data in add_indicator_data.value:
                if base_data.is_raw:
                    continue
                add_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = base_data.value

        if remove_indicator_data is not None:
            for base_data in remove_indicator_data.value:
                if base_data.is_raw:
                    continue
                remove_axis_data[
                    f"{base_data.year}-{base_data.month:02}"
                ] = -base_data.value

        if len(add_axis_data) > len(remove_axis_data):
            monthes = list(add_axis_data.keys())
        else:
            monthes = list(remove_axis_data.keys())

        add_x = []
        add_y = []
        remove_x = []
        remove_y = []
        for month in monthes:
            add_x.append(month)
            add_y.append(add_axis_data.get(month, 0))
            remove_x.append(month)
            remove_y.append(remove_axis_data.get(month, 0))

        if add_indicator_data is None:
            add_x = []
            add_y = []

        if remove_indicator_data is None:
            remove_x = []
            remove_y = []

        return add_x, add_y, remove_x, remove_y

    def export(self) -> t.List[ExportData]:
        if len(self.indicator_datum) == 0:
            return []

        line = Line(init_opts=opts.InitOpts(aria_opts=opts.AriaOpts(is_enable=True)))
        add_x, add_y, remove_x, remove_y = self.__all_data

        has_add = len(add_x) > 0
        has_remove = len(remove_x) > 0

        has_x = False
        if has_add:
            if not has_x:
                line.add_xaxis(xaxis_data=add_x)
                has_x = True
            line.add_yaxis(
                "Added Lines",
                add_y,
                label_opts=opts.LabelOpts(is_show=False),
                symbol="none",
                areastyle_opts=opts.AreaStyleOpts(color="green", opacity=0.5),
            )

        if has_remove:
            if not has_x:
                line.add_xaxis(xaxis_data=remove_x)
                has_x = True
            line.add_yaxis(
                "Removed Lines",
                remove_y,
                label_opts=opts.LabelOpts(is_show=False),
                symbol="none",
                areastyle_opts=opts.AreaStyleOpts(color="red", opacity=0.5),
            )

        line.set_global_opts(legend_opts=opts.LegendOpts(is_show=False))

        return [ExportData(name="Code Change Lines", chart=line, extra_data=analyze_indicators_data(self.indicator_datum))]  # type: ignore


@register_exporter
class NetworkExporter(BaseChartExporter):
    exporter_name = "network_exporter"
    accepted_indicator_dataclass = [DeveloperNetworkData, RepoNetworkData]

    def export(self) -> t.List[ExportData]:
        export_datum = []

        for indicator_data in self.indicator_datum:
            nodes = [
                {
                    "id": node.name,
                    "name": node.name,
                    "value": node.value,
                    "symbolSize": math.log(node.value + 1) * 10,
                }
                for node in indicator_data.value.nodes
            ]
            edges = [
                {"source": edge.name0, "target": edge.name1, "value": edge.value / 100}
                for edge in indicator_data.value.edges
            ]

            export_datum.append(
                ExportData(
                    name=get_indicator_title(indicator_data.name),
                    chart=Graph(init_opts=opts.InitOpts(height="1200px")).add(
                        "",
                        nodes,
                        edges,
                        repulsion=400,
                        edge_length=[50, 300],  # type: ignore
                        is_layout_animation=False,
                        layout="force",
                        label_opts=opts.LabelOpts(is_show=True),
                        is_roam=True,
                    ),
                )
            )
        return export_datum


class ProjectOpenRankGraph(Base):
    def __init__(self, graph_data: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._component_type = "project_openrank"
        self.html_content = base64.b64encode(
            self.render_embed(
                "project_openrank_network.html", env=JINJA_ENV, graph_data=graph_data
            ).encode()
        ).decode()


@register_exporter
class ProjectOpenRankNetworkExporter(BaseChartExporter):
    exporter_name = "project_openrank_network_exporter"
    accepted_indicator_dataclass = [ProjectOpenRankNetworkData]

    def export(self) -> t.List[ExportData]:
        exporter_datum = []
        for indicator_data in self.indicator_datum:
            for base_data in indicator_data.value:
                if base_data.value is None:
                    continue
                exporter_datum.append(
                    ExportData(
                        name=f"{get_indicator_title(indicator_data.name)}: {base_data.year}-{base_data.month:02}",
                        chart=ProjectOpenRankGraph(
                            graph_data=str(asdict(base_data.value))
                        ),
                    )
                )
        return exporter_datum
