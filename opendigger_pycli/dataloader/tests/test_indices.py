from opendigger_pycli.dataloader.indices import (
    ActivityRepoDataloader,
    ActivityUserDataLoader,
    AttentionRepoDataloader,
    OpenRankRepoDataloader,
    OpenRankUserDataLoader,
)

from . import TEST_ORG, TEST_REPO, TEST_USER_NAME

def test_openrank():
    '''
    Test index type: OpenRank value
    :return:
    '''
    # Create an instance of OpenRankRepoDataloader for loading repository data
    openrank_dataloader = OpenRankRepoDataloader()
    # Attempt to load data for the test organization and repository to ensure successful loading
    success_data = openrank_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success  # Assert that data loading is successful

    # Attempt to load data for a non-existent repository to ensure loading failure
    fail_data = openrank_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success  # Assert that data loading fails

    # Create an instance of OpenRankUserDataLoader for loading user data
    openrank_user_dataloader = OpenRankUserDataLoader()
    # Attempt to load data for the test username to ensure successful loading
    success_data = openrank_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    # Attempt to load data for a non-existent user to ensure loading failure
    fail_data = openrank_user_dataloader.load("not-exist-user")
    assert not fail_data.is_success


def test_activity():
    '''
    Test index type: activity, monthly activity of the project
    :return:
    '''
    activity_dataloader = ActivityRepoDataloader()
    # Attempt to load activity data for the test organization and repository to ensure successful loading
    success_data = activity_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success  # Assert that activity data loading is successful

    # Attempt to load activity data for a non-existent repository to ensure loading failure
    fail_data = activity_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success  # Assert that activity data loading fails

    # Create an instance of ActivityUserDataLoader for loading user activity data
    activity_user_dataloader = ActivityUserDataLoader()

    # Attempt to load activity data for the test username to ensure successful loading
    success_data = activity_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success  # Assert that user activity data loading is successful

    # Attempt to load activity data for a non-existent user to ensure loading failure
    fail_data = activity_user_dataloader.load("not-exist-user")
    assert not fail_data.is_success  # Assert that user activity data loading fails


def test_attention():
    '''
    Test index type: attention, monthly attention of the project
    :return:
    '''
    # Create an instance of AttentionRepoDataloader for loading attention data
    attention_dataloader = AttentionRepoDataloader()

    # Attempt to load attention data for the test organization and repository to ensure successful loading
    success_data = attention_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success  # Assert that attention data loading is successful

    # Attempt to load attention data for a non-existent repository to ensure loading failure
    fail_data = attention_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success  # Assert that attention data loading fails
