from dataclasses import dataclass
from typing import ClassVar, List

from .base import (
    BaseData,
    NameAndValue,
    NonTrivialIndicatorDict,
    NonTrivialIndicatorData,
    TrivialIndicatorData,
)


@dataclass
class ActiveDateAndTimeData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-activity-dates-and-times/
    """

    name: ClassVar[str] = "active_dates_and_times"
    value: List[BaseData[List[int]]]


@dataclass
class StarData(TrivialIndicatorData):
    name: ClassVar[str] = "stars"
    value: List[BaseData[int]]


@dataclass
class TechnicalForkData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-technical-fork/
    """

    name: ClassVar[str] = "technical_fork"
    value: List[BaseData[int]]


@dataclass
class ParticipantData(TrivialIndicatorData):
    name: ClassVar[str] = "participants"
    value: List[BaseData[int]]


@dataclass
class NewContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-new-contributors/
    """

    name: ClassVar[str] = "new_contributors_detail"
    value: List[BaseData[List[str]]]


@dataclass
class InactiveContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-inactive-contributors/
    """

    name: ClassVar[str] = "inactive_contributors"
    value: List[BaseData[int]]


@dataclass
class BusFactorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-bus-factor/
    """

    name: ClassVar[str] = "bus_factor_detail"
    value: List[BaseData[List[NameAndValue]]]


@dataclass
class NewIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-new/
    """

    name: ClassVar[str] = "issues_new"
    value: List[BaseData[int]]


@dataclass
class ClosedIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-closed/
    """

    name: ClassVar[str] = "issues_closed"
    value: List[BaseData[int]]


@dataclass
class IssueCommentData(TrivialIndicatorData):
    name: ClassVar[str] = "issue_comments"
    value: List[BaseData[int]]


@dataclass
class IssueResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "issue_response_time"
    value: NonTrivialIndicatorDict


@dataclass
class IssueResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "issue_resolution_duration"
    value: NonTrivialIndicatorDict


@dataclass
class IssueAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "issue_age"
    value: NonTrivialIndicatorDict


@dataclass
class AddedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_add"
    value: List[BaseData[int]]


@dataclass
class RemovedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    """

    name: ClassVar[str] = "code_change_lines_remove"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests/
    """

    name: ClassVar[str] = "change_requests"
    value: List[BaseData[int]]


@dataclass
class AcceptedChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests-accepted/
    """

    name: ClassVar[str] = "change_requests_accepted"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestReviewData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-request-reviews/
    """

    name: ClassVar[str] = "change_requests_reviews"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    """

    name: ClassVar[str] = "change_request_response_time"
    value: NonTrivialIndicatorDict


@dataclass
class ChangeRequestResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    """

    name: ClassVar[str] = "change_request_resolution_duration"
    value: NonTrivialIndicatorDict


@dataclass
class ChangeRequestAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    """

    name: ClassVar[str] = "change_request_age"
    value: NonTrivialIndicatorDict
