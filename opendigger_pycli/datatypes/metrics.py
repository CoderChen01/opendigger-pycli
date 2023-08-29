from dataclasses import dataclass
from typing import ClassVar

from .base import NonTrivialIndicatorData, TrivialIndicatorData


@dataclass
class ActiveDateAndTimeData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-activity-dates-and-times/
    """

    name: ClassVar[str] = "active_dates_and_times"


@dataclass
class StarData(TrivialIndicatorData):
    name: ClassVar[str] = "stars"


@dataclass
class TechnicalForkData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-technical-fork/
    """

    name: ClassVar[str] = "technical_fork"


@dataclass
class ParticipantData(TrivialIndicatorData):
    name: ClassVar[str] = "participants"


@dataclass
class NewContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-new-contributors/
    """

    name: ClassVar[str] = "new_contributors_detail"


@dataclass
class InactiveContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-inactive-contributors/
    """

    name: ClassVar[str] = "inactive_contributors"


@dataclass
class BusFactorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-bus-factor/
    """

    name: ClassVar[str] = "bus_factor_detail"


@dataclass
class NewIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-new/
    """

    name: ClassVar[str] = "issues_new"


@dataclass
class ClosedIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-closed/
    """

    name: ClassVar[str] = "issues_closed"


@dataclass
class IssueCommentData(TrivialIndicatorData):
    name: ClassVar[str] = "issue_comments"


@dataclass
class IssueResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "issue_response_time"


@dataclass
class IssueResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "issue_resolution_duration"


@dataclass
class IssueAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "issue_age"


@dataclass
class AddedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_add"


@dataclass
class RemovedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_remove"


@dataclass
class SumCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_sum"


@dataclass
class ChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests/
    """

    name: ClassVar[str] = "change_requests"


@dataclass
class AcceptedChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests-accepted/
    """

    name: ClassVar[str] = "change_requests_accepted"


@dataclass
class ChangeRequestReviewData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-request-reviews/
    """

    name: ClassVar[str] = "change_requests_reviews"


@dataclass
class ChangeRequestResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "change_request_response_time"


@dataclass
class ChangeRequestResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "change_request_resolution_duration"


@dataclass
class ChangeRequestAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "change_request_age"
