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
    get_repo_data,
    load_base_data,
    load_name_and_value,
    load_non_trival_metric_data,
    register_dataloader,
)


@register_dataloader
class ActiveDateAndTimeRepoDataloader(
    BaseRepoDataloader[ActiveDateAndTimeData]
):
    '''
    Data loader for Active Date and Time repository data.
    '''
    name = "active_date_and_time"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ActiveDateAndTimeData]:
        '''
        Load Active Date and Time repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ActiveDateAndTimeData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for Star repository data.
    '''
    name = "star"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[StarData]:
        '''
        Load Star repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[StarData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for Technical Fork repository data.
    '''
    name = "technical_fork"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[TechnicalForkData]:
        '''
        Load Technical Fork repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[TechnicalForkData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for Participant repository data.
    '''
    name = "participant"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[ParticipantData]:
        '''
        Load Participant repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ParticipantData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for NewContributor repository data.
    '''
    name = "new_contributor"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[NewContributorData]:
        '''
        Load NewContributor repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[NewContributorData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for InactiveContributor repository data.
    '''
    name = "inactive_contributor"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[InactiveContributorData]:
        '''
        Load InactiveContributor repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[InactiveContributorData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for BusFactor repository data.
    '''
    name = "bus_factor"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[BusFactorData]:
        '''
        Load BusFactor repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[BusFactorData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for NewIssue repository data.
    '''
    name = "new_issue"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[NewIssueData]:
        '''
        Load NewIssue repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[NewIssueData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ClosedIssue repository data.
    '''
    name = "closed_issue"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[ClosedIssueData]:
        '''
        Load ClosedIssue repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ClosedIssueData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for IssueComment repository data.
    '''
    name = "issue_comment"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[IssueCommentData]:
        '''
        Load IssueComment repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[IssueCommentData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for IssueResponseTime repository data.
    '''
    name = "issue_response_time"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[IssueResponseTimeData]:
        '''
        Load IssueResponseTime repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[IssueResponseTimeData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for IssueResolutionDuration repository data.
    '''
    name = "issue_resolution_duration"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[IssueResolutionDurationData]:
        '''
        Load IssueResolutionDuration repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[IssueResolutionDurationData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for IssueAge repository data.
    '''
    name = "issue_age"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[IssueAgeData]:
        '''
        Load IssueAge repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[IssueAgeData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for AddedCodeChangeLine repository data.
    '''
    name = "added_code_change_line"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[AddedCodeChangeLineData]:
        '''
        Load AddedCodeChangeLine repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[AddedCodeChangeLineData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for RemovedCodeChangeLine repository data.
    '''
    name = "removed_code_change_line"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[RemovedCodeChangeLineData]:
        '''
        Load RemovedCodeChangeLine repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[RemovedCodeChangeLineData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ChangeRequest repository data.
    '''
    name = "change_request"
    metric_type = "metric"

    def load(self, org: str, repo: str) -> DataloaderState[ChangeRequestData]:
        '''
        Load ChangeRequest repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ChangeRequestData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for AcceptedChangeRequest repository data.
    '''
    name = "accepted_change_request"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[AcceptedChangeRequestData]:
        '''
        Load AcceptedChangeRequest repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[AcceptedChangeRequestData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ChangeRequestReview repository data.
    '''
    name = "change_request_review"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestReviewData]:
        '''
        Load ChangeRequestReview repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ChangeRequestReviewData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ChangeRequestResponseTime repository data.
    '''
    name = "change_request_response_time"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestResponseTimeData]:
        '''
        Load ChangeRequestResponseTime repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ChangeRequestResponseTimeData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ChangeRequestResolutionDuration repository data.
    '''
    name = "change_request_resolution_duration"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestResolutionDurationData]:
        '''
        Load ChangeRequestResolutionDuration repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ChangeRequestResolutionDurationData]: The state of the data loading operation.
        '''
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
    '''
    Data loader for ChangeRequestAge repository data.
    '''
    name = "change_request_age"
    metric_type = "metric"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[ChangeRequestAgeData]:
        '''
        Load ChangeRequestAge repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ChangeRequestAgeData]: The state of the data loading operation.
        '''
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
