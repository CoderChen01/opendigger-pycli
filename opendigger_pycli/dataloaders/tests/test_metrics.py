from opendigger_pycli.dataloaders.metrics import (
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


def test_star():
    star_dataloader = StarRepoDataloader()
    success_data = star_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = star_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_active_date_and_time():
    active_date_and_time_dataloader = ActiveDateAndTimeRepoDataloader()
    success_data = active_date_and_time_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = active_date_and_time_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_added_code_change_line():
    added_code_change_line_dataloader = AddedCodeChangeLineRepoDataloader()
    success_data = added_code_change_line_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = added_code_change_line_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_removed_code_change_line():
    removed_code_change_line_dataloader = RemovedCodeChangeLineRepoDataloader()
    success_data = removed_code_change_line_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = removed_code_change_line_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_age():
    issue_age_dataloader = IssueAgeRepoDataloader()
    success_data = issue_age_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = issue_age_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_new_issue():
    new_issue_dataloader = NewIssueRepoDataloader()
    success_data = new_issue_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = new_issue_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_bus_factor():
    bus_factor_dataloader = BusFactorRepoDataloader()
    success_data = bus_factor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = bus_factor_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_closed_issue():
    closed_issue_dataloader = ClosedIssueRepoDataloader()
    success_data = closed_issue_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = closed_issue_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_participant():
    participant_dataloader = ParticipantRepoDataloader()
    success_data = participant_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = participant_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_resolution_duration():
    issue_resolution_duration_dataloader = IssueResolutionDurationRepoDataloader()
    success_data = issue_resolution_duration_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = issue_resolution_duration_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_comment():
    issue_comment_dataloader = IssueCommentRepoDataloader()
    success_data = issue_comment_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = issue_comment_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_change_request():
    change_request_dataloader = ChangeRequestRepoDataloader()
    success_data = change_request_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = change_request_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_technical_fork():
    technical_fork_dataloader = TechnicalForkRepoDataloader()
    success_data = technical_fork_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = technical_fork_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_new_contributor():
    new_contributor_dataloader = NewContributorRepoDataloader()
    success_data = new_contributor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = new_contributor_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_change_request_age():
    change_request_age_dataloader = ChangeRequestAgeRepoDataloader()
    success_data = change_request_age_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = change_request_age_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_issue_response_time():
    issue_response_time_dataloader = IssueResponseTimeRepoDataloader()
    success_data = issue_response_time_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = issue_response_time_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_change_request_review():
    change_request_review_dataloader = ChangeRequestReviewRepoDataloader()
    success_data = change_request_review_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = change_request_review_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_inactive_contributor():
    inactive_contributor_dataloader = InactiveContributorRepoDataloader()
    success_data = inactive_contributor_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = inactive_contributor_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_accepted_change_request():
    accepted_change_request_dataloader = AcceptedChangeRequestRepoDataloader()
    success_data = accepted_change_request_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = accepted_change_request_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_change_request_response_time():
    change_request_response_time_dataloader = ChangeRequestResponseTimeRepoDataloader()
    success_data = change_request_response_time_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = change_request_response_time_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success


def test_change_request_resolution_duration():
    change_request_resolution_duration_dataloader = (
        ChangeRequestResolutionDurationRepoDataloader()
    )
    success_data = change_request_resolution_duration_dataloader.load(
        TEST_ORG, TEST_REPO
    )
    assert success_data.is_success

    fail_data = change_request_resolution_duration_dataloader.load(
        TEST_ORG, "non-exist-repo"
    )
    assert not fail_data.is_success
