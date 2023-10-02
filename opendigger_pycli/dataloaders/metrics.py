import typing as t

from opendigger_pycli.datatypes import (
    AcceptedChangeRequestData,
    ActiveDateAndTimeData,
    AddedCodeChangeLineData,
    BusFactorData,
    ChangeRequestAgeData,
    ChangeRequestData,
    ChangeRequestResolutionDurationData,
    ChangeRequestResponseTimeData,
    ChangeRequestReviewData,
    ClosedIssueData,
    DataloaderResult,
    InactiveContributorData,
    IssueAgeData,
    IssueCommentData,
    IssueResolutionDurationData,
    IssueResponseTimeData,
    NewContributorData,
    NewIssueData,
    ParticipantData,
    RemovedCodeChangeLineData,
    StarData,
    SumCodeChangeLineData,
    TechnicalForkData,
    ActivityDetailData,
)

from .base import BaseRepoDataloader, register_dataloader
from .utils import (
    get_repo_data,
    load_base_data,
    load_name_and_value,
    load_non_trival_indicator_data,
)

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.dataloader import DataloaderProto


@register_dataloader
class ActiveDateAndTimeRepoDataloader(BaseRepoDataloader):
    name = "active_date_and_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/active_dates_and_times.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ActiveDateAndTimeData]:
        data = get_repo_data(org, repo, ActiveDateAndTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActiveDateAndTimeData(
                value=load_base_data(data, lambda x: [int(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class StarRepoDataloader(BaseRepoDataloader):
    name = "star"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/stars.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[StarData]:
        data = get_repo_data(org, repo, StarData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=StarData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class TechnicalForkRepoDataloader(BaseRepoDataloader):
    name = "technical_fork"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/technical_fork.json"

    def load(self, org: str, repo: str) -> DataloaderResult[TechnicalForkData]:
        data = get_repo_data(org, repo, TechnicalForkData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=TechnicalForkData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class ParticipantRepoDataloader(BaseRepoDataloader):
    name = "participant"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/participants.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ParticipantData]:
        data = get_repo_data(org, repo, ParticipantData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ParticipantData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class NewContributorRepoDataloader(BaseRepoDataloader):
    name = "new_contributor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/new_contributors_detail.json"

    def load(self, org: str, repo: str) -> DataloaderResult[NewContributorData]:
        data = get_repo_data(org, repo, NewContributorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=NewContributorData(
                value=load_base_data(data, lambda x: [str(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class InactiveContributorRepoDataloader(BaseRepoDataloader):
    name = "inactive_contributor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/inactive_contributors.json"

    def load(self, org: str, repo: str) -> DataloaderResult[InactiveContributorData]:
        data = get_repo_data(org, repo, InactiveContributorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=InactiveContributorData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class BusFactorRepoDataloader(BaseRepoDataloader):
    name = "bus_factor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/bus_factor_detail.json"

    def load(self, org: str, repo: str) -> DataloaderResult[BusFactorData]:
        data = get_repo_data(org, repo, BusFactorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=BusFactorData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )


@register_dataloader
class NewIssueRepoDataloader(BaseRepoDataloader):
    name = "new_issue"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_new.json"

    def load(self, org: str, repo: str) -> DataloaderResult[NewIssueData]:
        data = get_repo_data(org, repo, NewIssueData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=NewIssueData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class ClosedIssueRepoDataloader(BaseRepoDataloader):
    name = "closed_issue"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_closed.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ClosedIssueData]:
        data = get_repo_data(org, repo, ClosedIssueData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ClosedIssueData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class IssueCommentRepoDataloader(BaseRepoDataloader):
    name = "issue_comment"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_comments.json"

    def load(self, org: str, repo: str) -> DataloaderResult[IssueCommentData]:
        data = get_repo_data(org, repo, IssueCommentData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueCommentData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class IssueResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "issue_response_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_response_time.json"

    def load(self, org: str, repo: str) -> DataloaderResult[IssueResponseTimeData]:
        data = get_repo_data(org, repo, IssueResponseTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueResponseTimeData(value=load_non_trival_indicator_data(data)),
            desc="",
        )


@register_dataloader
class IssueResolutionDurationRepoDataloader(BaseRepoDataloader):
    name = "issue_resolution_duration"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_resolution_duration.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[IssueResolutionDurationData]:
        data = get_repo_data(org, repo, IssueResolutionDurationData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueResolutionDurationData(
                value=load_non_trival_indicator_data(data)
            ),
            desc="",
        )


@register_dataloader
class IssueAgeRepoDataloader(BaseRepoDataloader):
    name = "issue_age"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_age.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[IssueAgeData]:
        data = get_repo_data(org, repo, IssueAgeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueAgeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


@register_dataloader
class AddedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "added_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_add.json"

    def load(self, org: str, repo: str) -> DataloaderResult[AddedCodeChangeLineData]:
        data = get_repo_data(org, repo, AddedCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=AddedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class RemovedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "removed_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_remove.json"

    def load(self, org: str, repo: str) -> DataloaderResult[RemovedCodeChangeLineData]:
        data = get_repo_data(org, repo, RemovedCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=RemovedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class SummedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "summed_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_sum.json"

    def load(self, org: str, repo: str) -> DataloaderResult[SumCodeChangeLineData]:
        data = get_repo_data(org, repo, SumCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=SumCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "change_request"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestData]:
        data = get_repo_data(org, repo, ChangeRequestData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class AcceptedChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "accepted_change_request"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_accepted.json"

    def load(self, org: str, repo: str) -> DataloaderResult[AcceptedChangeRequestData]:
        data = get_repo_data(org, repo, AcceptedChangeRequestData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=AcceptedChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestReviewRepoDataloader(BaseRepoDataloader):
    name = "change_request_review"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_reviews.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestReviewData]:
        data = get_repo_data(org, repo, ChangeRequestReviewData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestReviewData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "change_request_response_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_response_time.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[ChangeRequestResponseTimeData]:
        data = get_repo_data(org, repo, ChangeRequestResponseTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestResponseTimeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestResolutionDurationRepoDataloader(BaseRepoDataloader):
    name = "change_request_resolution_duration"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_resolution_duration.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[ChangeRequestResolutionDurationData]:
        data = get_repo_data(org, repo, ChangeRequestResolutionDurationData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestResolutionDurationData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestAgeRepoDataloader(BaseRepoDataloader):
    name = "change_request_age"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_age.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestAgeData]:
        data = get_repo_data(org, repo, ChangeRequestAgeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestAgeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


@register_dataloader
class ActivityDetailRepoDataloader(BaseRepoDataloader):
    name = "activity_detail"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/activity_details.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ActivityDetailData]:
        data = get_repo_data(org, repo, ActivityDetailData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActivityDetailData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )
