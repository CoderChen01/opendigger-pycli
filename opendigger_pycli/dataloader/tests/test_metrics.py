from opendigger_pycli.dataloader.metrics import (
    AcceptedChangeRequestRepoDataloader,
    ActiveDateAndTimeRepoDataloader,
    AddedCodeChangeLineRepoDataloader,
    BusFactorRepoDataloader,
    ChangeRequestAgeRepoDataloader,
    ChangeRequestRepoDataloader,
    ChangeRequestResolutionDurationRepoDataloader,
    ChangeRequestResponseTimeRepoDataloader,
    ChangeRequestReviewRepoDataloader,
    ClosedIssueRepoDataloader,
    InactiveContributorRepoDataloader,
    IssueAgeRepoDataloader,
    IssueCommentRepoDataloader,
    IssueResolutionDurationRepoDataloader,
    IssueResponseTimeRepoDataloader,
    NewContributorRepoDataloader,
    NewIssueRepoDataloader,
    ParticipantRepoDataloader,
    RemovedCodeChangeLineRepoDataloader,
    StarRepoDataloader,
    TechnicalForkRepoDataloader,
)

from . import TEST_ORG, TEST_REPO


def test_active_date_and_time():
    '''
    daily project activity
    :return:
    '''
    # Create an instance of ActiveDateAndTimeRepoDataloader for loading daily activity data
    active_date_and_time_dataloader = ActiveDateAndTimeRepoDataloader()

    # Load daily activity data for the test organization and repository
    success_data = active_date_and_time_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = active_date_and_time_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_star():
    '''
    Test index type: number of stars for the project
    :return:
    '''
    # Create an instance of StarRepoDataloader for loading star count data
    star_dataloader = StarRepoDataloader()

    # Load star count data for the test organization and repository
    success_data = star_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = star_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_technical_fork():
    '''
    Test index type: number of forks for the project
    :return:
    '''
    # Create an instance of TechnicalForkRepoDataloader for loading fork count data
    technical_fork_dataloader = TechnicalForkRepoDataloader()

    # Load fork count data for the test organization and repository
    success_data = technical_fork_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = technical_fork_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_participant():
    '''
    Test index type: number of participants for the project
    :return:
    '''
    # Create an instance of ParticipantRepoDataloader for loading participant count data
    participant_dataloader = ParticipantRepoDataloader()

    # Load participant count data for the test organization and repository
    success_data = participant_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = participant_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_new_contributor():
    '''
    list of newly added contributors
    :return:
    '''
    # Create an instance of NewContributorRepoDataloader for loading new contributor data
    new_contributor_dataloader = NewContributorRepoDataloader()

    # Load new contributor data for the test organization and repository
    success_data = new_contributor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = new_contributor_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_inactive_contributor():
    '''
    number of inactive developers
    :return:
    '''
    # Create an instance of InactiveContributorRepoDataloader for loading inactive contributor count data
    inactive_contributor_dataloader = InactiveContributorRepoDataloader()

    # Load inactive contributor count data for the test organization and repository
    success_data = inactive_contributor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = inactive_contributor_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


# Bus factor
def test_bus_factor():
    '''
    bus factor per month for the project
    :return:
    '''
    # Create an instance of BusFactorRepoDataloader for loading bus factor data
    bus_factor_dataloader = BusFactorRepoDataloader()

    # Load bus factor data per month for the test organization and repository
    success_data = bus_factor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = bus_factor_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


# Test for bus factor detail


# Issue
def test_new_issue():
    '''
    number of newly created issues
    :return:
    '''
    # Create an instance of NewIssueRepoDataloader for loading new issue count data
    new_issue_dataloader = NewIssueRepoDataloader()

    # Load new issue count data for the test organization and repository
    success_data = new_issue_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = new_issue_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_closed_issue():
    '''
    number of closed issues
    :return:
    '''
    # Create an instance of ClosedIssueRepoDataloader for loading closed issue count data
    closed_issue_dataloader = ClosedIssueRepoDataloader()

    # Load closed issue count data for the test organization and repository
    success_data = closed_issue_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = closed_issue_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_comment():
    '''
    number of comments on issues
    :return:
    '''
    # Create an instance of IssueCommentRepoDataloader for loading issue comment count data
    issue_comment_dataloader = IssueCommentRepoDataloader()

    # Load issue comment count data for the test organization and repository
    success_data = issue_comment_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = issue_comment_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_response_time():
    '''
    duration from issue creation to first response
    :return:
    '''
    # Create an instance of IssueResponseTimeRepoDataloader for loading issue response time data
    issue_response_time_dataloader = IssueResponseTimeRepoDataloader()

    # Load issue response time data for the test organization and repository
    success_data = issue_response_time_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = issue_response_time_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_resolution_duration():
    '''
    duration from issue creation to closure
    :return:
    '''
    # Create an instance of IssueResolutionDurationRepoDataloader for loading issue resolution duration data
    issue_resolution_duration_dataloader = IssueResolutionDurationRepoDataloader()

    # Load issue resolution duration data for the test organization and repository
    success_data = issue_resolution_duration_dataloader.load(
        TEST_ORG, TEST_REPO
    )
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = issue_resolution_duration_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_issue_age():
    '''
    age of open issues (assumed until March 23rd)
    :return:
    '''
    # Create an instance of IssueAgeRepoDataloader for loading issue age data
    issue_age_dataloader = IssueAgeRepoDataloader()

    # Load issue age data for the test organization and repository
    success_data = issue_age_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = issue_age_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


# Code change lines
def test_added_code_change_line():
    '''
    number of lines added in code changes
    :return:
    '''
    # Create an instance of AddedCodeChangeLineRepoDataloader for loading added code change line data
    added_code_change_line_dataloader = AddedCodeChangeLineRepoDataloader()

    # Load added code change line data for the test organization and repository
    success_data = added_code_change_line_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = added_code_change_line_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_removed_code_change_line():
    '''
    Test index type: number of lines removed in code changes
    :return:
    '''
    # Create an instance of RemovedCodeChangeLineRepoDataloader for loading removed code change line data
    removed_code_change_line_dataloader = RemovedCodeChangeLineRepoDataloader()

    # Load removed code change line data for the test organization and repository
    success_data = removed_code_change_line_dataloader.load(
        TEST_ORG, TEST_REPO
    )
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = removed_code_change_line_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_change_request():
    '''
    Test index type: number of change requests (PRs)
    :return:
    '''
    # Create an instance of ChangeRequestRepoDataloader for loading change request data
    change_request_dataloader = ChangeRequestRepoDataloader()

    # Load change request data for the test organization and repository
    success_data = change_request_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = change_request_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_accepted_change_request():
    '''
    number of accepted change requests (merged PRs)
    :return:
    '''
    # Create an instance of AcceptedChangeRequestRepoDataloader for loading accepted change request data
    accepted_change_request_dataloader = AcceptedChangeRequestRepoDataloader()

    # Load accepted change request data for the test organization and repository
    success_data = accepted_change_request_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = accepted_change_request_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_change_request_review():
    '''
    number of reviewers in change requests (PRs)
    :return:
    '''
    # Create an instance of ChangeRequestReviewRepoDataloader for loading change request review data
    change_request_review_dataloader = ChangeRequestReviewRepoDataloader()

    # Load change request review data for the test organization and repository
    success_data = change_request_review_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = change_request_review_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_change_request_response_time():
    '''
    response time of change requests (PRs) from creation to first response
    :return:
    '''
    # Create an instance of ChangeRequestResponseTimeRepoDataloader for loading change request response time data
    change_request_response_time_dataloader = (
        ChangeRequestResponseTimeRepoDataloader()
    )

    # Load change request response time data for the test organization and repository
    success_data = change_request_response_time_dataloader.load(
        TEST_ORG, TEST_REPO
    )
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = change_request_response_time_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_change_request_resolution_duration():
    '''
    duration of change requests (PRs) from creation to resolution (closure)
    :return:
    '''
    # Create an instance of ChangeRequestResolutionDurationRepoDataloader for loading change request resolution duration data
    change_request_resolution_duration_dataloader = (
        ChangeRequestResolutionDurationRepoDataloader()
    )

    # Load change request resolution duration data for the test organization and repository
    success_data = change_request_resolution_duration_dataloader.load(
        TEST_ORG, TEST_REPO
    )
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = change_request_resolution_duration_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success


def test_change_request_age():
    '''
    age/lifetime of change requests (PRs) until the current date (assuming open PRs until March 23rd, 2023)
    :return:
    '''
    # Create an instance of ChangeRequestAgeRepoDataloader for loading change request age data
    change_request_age_dataloader = ChangeRequestAgeRepoDataloader()

    # Load change request age data for the test organization and repository
    success_data = change_request_age_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load data for a non-existing repository to test failure case
    fail_data = change_request_age_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success

# test_activity_details()
