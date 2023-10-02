from dataclasses import dataclass
from typing import ClassVar, List

from .base import (
    BaseData,
    NameAndValue,
    NonTrivialIndicatorData,
    TimeDurationRelatedIndicatorDict,
    TrivialIndicatorData,
)


@dataclass
class ActiveDateAndTimeData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-activity-dates-and-times/
    Active Dates and Times is a metric proposed by CHAOSS
    that describes on which dates
    and times developers in the community are active
    """

    name: ClassVar[str] = "active_dates_and_times"
    value: List[BaseData[List[int]]]


@dataclass
class StarData(TrivialIndicatorData):
    """
    Number of stars per month for the project
    """

    name: ClassVar[str] = "stars"
    value: List[BaseData[int]]


@dataclass
class TechnicalForkData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-technical-fork/
    A technical fork is a distributed version control copy of a project.
    The number of technical forks indicates the number of copies
    of a project on the same code development platform.
    """

    name: ClassVar[str] = "technical_fork"
    value: List[BaseData[int]]


@dataclass
class ParticipantData(TrivialIndicatorData):
    """
    Participants is an indicator proposed by X-lab,
    which refers to developers who have generated log behaviors in the project.
    """

    name: ClassVar[str] = "participants"
    value: List[BaseData[int]]


@dataclass
class NewContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-new-contributors/
    New Contributors is a metric proposed by CHAOSS,
    see the documentation for details.
    It is implemented in OpenDigger for developers
    who have contributed code for the first time in a project.
    """

    name: ClassVar[str] = "new_contributors_detail"
    value: List[BaseData[List[str]]]


@dataclass
class InactiveContributorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-inactive-contributors/
    Inactive Contributors is a metric proposed by CHAOSS,
    see the documentation for details.
    It is implemented in OpenDigger for developers
    who have not contributed code to a project
    for a certain period of time (the exact length of time is a configurable parameter).
    """

    name: ClassVar[str] = "inactive_contributors"
    value: List[BaseData[int]]


@dataclass
class BusFactorData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-bus-factor/
    The Bus Factor is a compelling metric because it visualizes the question
    "how many contributors can we lose before a project stalls?"
    by hypothetically having these people get run over by a bus (more pleasantly,
    how many would have to win in a lottery and decide to move on).
    The Bus Factor is the smallest number of people that make 50% of contributions.
    """

    name: ClassVar[str] = "bus_factor_detail"
    value: List[BaseData[List[NameAndValue]]]


@dataclass
class NewIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-new/
    Issue New is an indicator proposed by CHAOSS.
    """

    name: ClassVar[str] = "issues_new"
    value: List[BaseData[int]]


@dataclass
class ClosedIssueData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issues-closed/
    Issue Close is a metric proposed by CHAOSS,
    see the documentation for details.
    """

    name: ClassVar[str] = "issues_closed"
    value: List[BaseData[int]]


@dataclass
class IssueCommentData(TrivialIndicatorData):
    """
    Issue Comment is a metric proposed by X-lab
    that refers to the total number of Issue comments in a project over time;
    """

    name: ClassVar[str] = "issue_comments"
    value: List[BaseData[int]]


@dataclass
class IssueResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    Issue Response Time is a metric proposed by CHAOSS,
    see the documentation for details.
    It refers to the average, median, etc.
    of the issues in a project over a period of time
    from the time they are raised to the first time they are responded to,
    and is a parameter that can be configured in OpenDigger.
    """

    name: ClassVar[str] = "issue_response_time"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class IssueResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    Issue Resolution Duration is a metric proposed by CHAOSS,
    see the documentation for details.
    It refers to the average, median, etc.
    of the issues in a project over a period of time,
    from the time they were raised to the time they were closed,
    and is a parameter that can be configured in OpenDigger.
    """

    name: ClassVar[str] = "issue_resolution_duration"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class IssueAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    This metric is an indication of how long issues have been left open in the considered time period.
    If an issue has been closed but re-opened again within that period
    if will be considered as having remained open since its initial opening date.
    """

    name: ClassVar[str] = "issue_age"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class AddedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    Code Changes Links is a CHAOSS proposed metric,
    see the documentation for details.
    The available filters are Add Lines of Code, Delete Lines of Code.
    """

    name: ClassVar[str] = "code_change_lines_add"
    value: List[BaseData[int]]


@dataclass
class RemovedCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    Code Changes Links is a CHAOSS proposed metric,
    see the documentation for details.
    The available filters are Add Lines of Code, Delete Lines of Code.
    """

    name: ClassVar[str] = "code_change_lines_remove"
    value: List[BaseData[int]]


@dataclass
class SumCodeChangeLineData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-code-changes-lines/
    Code Changes Links is a CHAOSS proposed metric,
    see the documentation for details.
    The available filters are Add Lines of Code, Delete Lines of Code.
    """

    name: ClassVar[str] = "code_change_lines_sum"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests/
    Change Requests is a metric proposed by CHAOSS,
    see the documentation for details.
    In the GitHub scenario, it is implemented as the number of PRs in OpenDigger.
    """

    name: ClassVar[str] = "change_requests"
    value: List[BaseData[int]]


@dataclass
class AcceptedChangeRequestData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-requests-accepted/
    Change Requests Accepted is a metric proposed by CHAOSS,
    see the documentation for details.
    In the GitHub scenario OpenDigger is implemented as the number of PR merged.
    """

    name: ClassVar[str] = "change_requests_accepted"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestReviewData(TrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-change-request-reviews/
    Change Requests reviews is a metric proposed by CHAOSS,
    see the documentation for details.
    In the GitHub scenario OpenDigger is implemented as the number of PR reviews.
    """

    name: ClassVar[str] = "change_requests_reviews"
    value: List[BaseData[int]]


@dataclass
class ChangeRequestResponseTimeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-response-time/
    Refers to the average, median, etc.
    of PRs in a project over a period of time
    from the time they were raised to the first time they were responded to,
    and is a configurable parameter in OpenDigger.
    """

    name: ClassVar[str] = "change_request_response_time"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class ChangeRequestResolutionDurationData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-resolution-duration/
    Refers to the mean, median, etc. of PRs in a project over time,
    from the time they were raised to the time they were closed,
    and is a configurable parameter in OpenDigger.
    """

    name: ClassVar[str] = "change_request_resolution_duration"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class ChangeRequestAgeData(NonTrivialIndicatorData):
    """
    ref: https://chaoss.community/metric-issue-age/
    This metric is an indication of how long PRs have been left open in the considered time period.
    If an PR has been closed but re-opened again within that period
    if will be considered as having remained open since its initial opening date.
    """

    name: ClassVar[str] = "change_request_age"
    value: TimeDurationRelatedIndicatorDict


@dataclass
class ActivityDetailData(TrivialIndicatorData):
    """
    ref: https://github.com/X-lab2017/open-digger/issues/1186
    Activity is a statistical metric proposed by the X-lab lab,
    weighted to take into account five collaborative event behaviors:
    issue comment, open issue, open pr, review pr, and pr merged.
    """

    name: ClassVar[str] = "activity_details"
    value: List[BaseData[List[NameAndValue]]]
