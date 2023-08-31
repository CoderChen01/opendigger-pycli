from opendigger_pycli.dataloaders.indices import (
    ActivityRepoDataloader,
    ActivityUserDataLoader,
    AttentionRepoDataloader,
    OpenRankRepoDataloader,
    OpenRankUserDataLoader,
)

from . import TEST_ORG, TEST_REPO, TEST_USER_NAME


def test_openrank():
    openrank_dataloader = OpenRankRepoDataloader()
    success_data = openrank_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = openrank_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success

    openrank_user_dataloader = OpenRankUserDataLoader()
    success_data = openrank_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    fail_data = openrank_user_dataloader.load("not-exist-user")
    assert not fail_data.is_success


def test_activity():
    activity_dataloader = ActivityRepoDataloader()
    success_data = activity_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = activity_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success

    activity_user_dataloader = ActivityUserDataLoader()
    success_data = activity_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    fail_data = activity_user_dataloader.load("not-exist-user")
    assert not fail_data.is_success


def test_attention():
    attention_dataloader = AttentionRepoDataloader()
    success_data = attention_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = attention_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success
