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
    TechnicalForkData,
)

from .base import (
    BaseRepoDataloader,
    DataloaderState,
    register_dataloader,
)
from .utils import (
    get_repo_data,
    load_base_data,
    load_name_and_value,
    load_non_trival_metric_data,
)


@register_dataloader
class ActiveDateAndTimeRepoDataloader(BaseRepoDataloader):
    name = "active_date_and_time"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/active_dates_and_times.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ActiveDateAndTimeData]:
        data = get_repo_data(org, repo, ActiveDateAndTimeData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=ActiveDateAndTimeData(
                value=load_base_data(data, lambda x: [int(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class StarRepoDataloader(BaseRepoDataloader):
    name = "star"
    metric_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/stars.json"

    def load(self, org: str, repo: str) -> DataloaderState[StarData]:
        data = get_repo_data(org, repo, StarData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=StarData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class TechnicalForkRepoDataloader(BaseRepoDataloader):
    name = "technical_fork"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/technical_fork.json"

    def load(self, org: str, repo: str) -> DataloaderState[TechnicalForkData]:
        data = get_repo_data(org, repo, TechnicalForkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=TechnicalForkData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class ParticipantRepoDataloader(BaseRepoDataloader):
    name = "participant"
    metric_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/participants.json"

    def load(self, org: str, repo: str) -> DataloaderState[ParticipantData]:
        data = get_repo_data(org, repo, ParticipantData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=ParticipantData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class NewContributorRepoDataloader(BaseRepoDataloader):
    name = "new_contributor"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/new_contributors_detail.json"

    def load(self, org: str, repo: str) -> DataloaderState[NewContributorData]:
        data = get_repo_data(org, repo, NewContributorData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=NewContributorData(
                value=load_base_data(data, lambda x: [str(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class InactiveContributorRepoDataloader(BaseRepoDataloader):
    name = "inactive_contributor"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/inactive_contributors.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[InactiveContributorData]:
        data = get_repo_data(org, repo, InactiveContributorData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=InactiveContributorData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class BusFactorRepoDataloader(BaseRepoDataloader):
    name = "bus_factor"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/bus_factor_detail.json"

    def load(self, org: str, repo: str) -> DataloaderState[BusFactorData]:
        data = get_repo_data(org, repo, BusFactorData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
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
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_new.json"

    def load(self, org: str, repo: str) -> DataloaderState[NewIssueData]:
        data = get_repo_data(org, repo, NewIssueData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=NewIssueData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class ClosedIssueRepoDataloader(BaseRepoDataloader):
    name = "closed_issue"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_closed.json"

    def load(self, org: str, repo: str) -> DataloaderState[ClosedIssueData]:
        data = get_repo_data(org, repo, ClosedIssueData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ClosedIssueData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class IssueCommentRepoDataloader(BaseRepoDataloader):
    name = "issue_comment"
    metric_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_comments.json"

    def load(self, org: str, repo: str) -> DataloaderState[IssueCommentData]:
        data = get_repo_data(org, repo, IssueCommentData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=IssueCommentData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class IssueResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "issue_response_time"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_response_time.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[IssueResponseTimeData]:
        data = get_repo_data(org, repo, IssueResponseTimeData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=IssueResponseTimeData(
                value=load_non_trival_metric_data(data)
            ),
            desc="",
        )


@register_dataloader
class IssueResolutionDurationRepoDataloader(BaseRepoDataloader):
    name = "issue_resolution_duration"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_resolution_duration.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[IssueResolutionDurationData]:
        data = get_repo_data(org, repo, IssueResolutionDurationData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=IssueResolutionDurationData(
                value=load_non_trival_metric_data(data)
            ),
            desc="",
        )


@register_dataloader
class IssueAgeRepoDataloader(BaseRepoDataloader):
    name = "issue_age"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_age.json"

    def load(self, org: str, repo: str) -> DataloaderState[IssueAgeData]:
        data = get_repo_data(org, repo, IssueAgeData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=IssueAgeData(
                value=load_non_trival_metric_data(data),
            ),
            desc="",
        )


@register_dataloader
class AddedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "added_code_change_line"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_add.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[AddedCodeChangeLineData]:
        data = get_repo_data(org, repo, AddedCodeChangeLineData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=AddedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class RemovedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "removed_code_change_line"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_remove.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[RemovedCodeChangeLineData]:
        data = get_repo_data(org, repo, RemovedCodeChangeLineData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=RemovedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "change_request"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests.json"

    def load(self, org: str, repo: str) -> DataloaderState[ChangeRequestData]:
        data = get_repo_data(org, repo, ChangeRequestData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class AcceptedChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "accepted_change_request"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_accepted.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[AcceptedChangeRequestData]:
        data = get_repo_data(org, repo, AcceptedChangeRequestData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=AcceptedChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestReviewRepoDataloader(BaseRepoDataloader):
    name = "change_request_review"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_reviews.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestReviewData]:
        data = get_repo_data(org, repo, ChangeRequestReviewData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ChangeRequestReviewData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "change_request_response_time"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_response_time.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestResponseTimeData]:
        data = get_repo_data(org, repo, ChangeRequestResponseTimeData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ChangeRequestResponseTimeData(
                value=load_non_trival_metric_data(data),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestResolutionDurationRepoDataloader(BaseRepoDataloader):
    name = "change_request_resolution_duration"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_resolution_duration.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestResolutionDurationData]:
        data = get_repo_data(
            org, repo, ChangeRequestResolutionDurationData.name
        )
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ChangeRequestResolutionDurationData(
                value=load_non_trival_metric_data(data),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestAgeRepoDataloader(BaseRepoDataloader):
    name = "change_request_age"
    metric_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_age.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestAgeData]:
        data = get_repo_data(org, repo, ChangeRequestAgeData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderState(
            is_success=True,
            data=ChangeRequestAgeData(
                value=load_non_trival_metric_data(data),
            ),
            desc="",
        )
