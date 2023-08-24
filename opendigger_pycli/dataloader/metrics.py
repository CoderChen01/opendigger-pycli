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
class ActiveDateAndTimeRepoDataloader(
    BaseRepoDataloader[ActiveDateAndTimeData]
):
    name = "active_date_and_time"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class StarRepoDataloader(BaseRepoDataloader[StarData]):
    name = "star"
    metric_type = "metric"
    introducer = "X-lab"

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
class TechnicalForkRepoDataloader(BaseRepoDataloader[TechnicalForkData]):
    name = "technical_fork"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ParticipantRepoDataloader(BaseRepoDataloader[ParticipantData]):
    name = "participant"
    metric_type = "metric"
    introducer = "X-lab"

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
class NewContributorRepoDataloader(BaseRepoDataloader[NewContributorData]):
    name = "new_contributor"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class InactiveContributorRepoDataloader(
    BaseRepoDataloader[InactiveContributorData]
):
    name = "inactive_contributor"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class BusFactorRepoDataloader(BaseRepoDataloader[BusFactorData]):
    name = "bus_factor"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class NewIssueRepoDataloader(BaseRepoDataloader[NewIssueData]):
    name = "new_issue"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ClosedIssueRepoDataloader(BaseRepoDataloader[ClosedIssueData]):
    name = "closed_issue"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class IssueCommentRepoDataloader(BaseRepoDataloader[IssueCommentData]):
    name = "issue_comment"
    metric_type = "metric"
    introducer = "X-lab"

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
class IssueResponseTimeRepoDataloader(
    BaseRepoDataloader[IssueResponseTimeData]
):
    name = "issue_response_time"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class IssueResolutionDurationRepoDataloader(
    BaseRepoDataloader[IssueResolutionDurationData]
):
    name = "issue_resolution_duration"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class IssueAgeRepoDataloader(BaseRepoDataloader[IssueAgeData]):
    name = "issue_age"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class AddedCodeChangeLineRepoDataloader(
    BaseRepoDataloader[AddedCodeChangeLineData]
):
    name = "added_code_change_line"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class RemovedCodeChangeLineRepoDataloader(
    BaseRepoDataloader[RemovedCodeChangeLineData]
):
    name = "removed_code_change_line"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ChangeRequestRepoDataloader(BaseRepoDataloader[ChangeRequestData]):
    name = "change_request"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class AcceptedChangeRequestRepoDataloader(
    BaseRepoDataloader[AcceptedChangeRequestData]
):
    name = "accepted_change_request"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ChangeRequestReviewRepoDataloader(
    BaseRepoDataloader[ChangeRequestReviewData]
):
    name = "change_request_review"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ChangeRequestResponseTimeRepoDataloader(
    BaseRepoDataloader[ChangeRequestResponseTimeData]
):
    name = "change_request_response_time"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ChangeRequestResolutionDurationRepoDataloader(
    BaseRepoDataloader[ChangeRequestResolutionDurationData]
):
    name = "change_request_resolution_duration"
    metric_type = "metric"
    introducer = "CHAOSS"

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
class ChangeRequestAgeRepoDataloader(BaseRepoDataloader[ChangeRequestAgeData]):
    name = "change_request_age"
    metric_type = "metric"
    introducer = "CHAOSS"

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
