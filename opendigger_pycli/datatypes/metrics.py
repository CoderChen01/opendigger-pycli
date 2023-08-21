from dataclasses import dataclass
from typing import ClassVar, List

from .base import BaseData, NameAndValue, NonTrivialMetricDict


@dataclass
class ActiveDateAndTimeData:
    """
    ref: https://chaoss.community/metric-activity-dates-and-times/
    """

    name: ClassVar[str] = "active_dates_and_times"
    value: List[BaseData[List[int]]]


@dataclass
class StarData:
    name: ClassVar[str] = "stars"
    value: List[BaseData[int]]


@dataclass
class TechnicalForkData:
    """
    ref: https://chaoss.community/metric-technical-fork/
    """

    name: ClassVar[str] = "technical_fork"
    value: List[BaseData[int]]


@dataclass
class ParticipantData:
    name: ClassVar[str] = "participants"
    value: List[BaseData[int]]


@dataclass
class NewContributorData:
    """
    ref: https://chaoss.community/metric-new-contributors/
    """

    name: ClassVar[str] = "new_contributors_detail"
    value: List[BaseData[List[str]]]


@dataclass
class InactiveContributorData:
    """
    ref: https://chaoss.community/metric-inactive-contributors/
    """

    name: ClassVar[str] = "inactive_contributors"
    value: List[BaseData[int]]


@dataclass
class BusFactorData:
    """
    ref: https://chaoss.community/metric-bus-factor/
    """

    name: ClassVar[str] = "bus_factor_detail"
    value: List[BaseData[List[NameAndValue]]]


@dataclass
class NewIssueData:
    """
    ref: https://chaoss.community/metric-issues-new/
    """

    name: ClassVar[str] = "issues_new"
    value: List[BaseData[int]]


@dataclass
class ClosedIssueData:
    """
    ref: https://chaoss.community/metric-issues-closed/
    """

    name: ClassVar[str] = "issues_closed"
    value: List[BaseData[int]]


@dataclass
class IssueCommentData:
    name: ClassVar[str] = "issue_comments"
    value: List[BaseData[int]]


@dataclass
class IssueResponseTimeData:
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "issue_response_time"
    value: NonTrivialMetricDict


@dataclass
class IssueResolutionDurationData:
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "issue_resolution_duration"
    value: NonTrivialMetricDict


@dataclass
class IssueAgeData:
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "issue_age"
    value: NonTrivialMetricDict


@dataclass
class AddedCodeChangeLineData:
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_add"
    value: List[BaseData[int]]


@dataclass
class RemovedCodeChangeLineData:
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_remove"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestData:
    """
    ref: https://chaoss.community/metric-change-requests/
    """

    name: ClassVar[str] = "change_requests"
    value: List[BaseData[int]]


@dataclass
class AcceptedChangeRequestData:
    """
    ref: https://chaoss.community/metric-change-requests-accepted/
    """

    name: ClassVar[str] = "change_requests_accepted"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestReviewData:
    """
    ref: https://chaoss.community/metric-change-request-reviews/
    """

    name: ClassVar[str] = "change_requests_reviews"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestResponseTimeData:
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "change_request_response_time"
    value: NonTrivialMetricDict


@dataclass
class ChangeRequestResolutionDurationData:
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "change_request_resolution_duration"
    value: NonTrivialMetricDict


@dataclass
class ChangeRequestAgeData:
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "change_request_age"
    value: NonTrivialMetricDict
