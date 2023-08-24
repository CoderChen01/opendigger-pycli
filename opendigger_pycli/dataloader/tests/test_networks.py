from opendigger_pycli.dataloader.networks import (
    DeveloperNetworkRepoDataloader,
    DeveloperNetworkUserDataloader,
    ProjectOpenRankNetworkRepoDataloader,
    RepoNetworkRepoDataloader,
    RepoNetworkUserDataloader,
)

from . import TEST_ORG, TEST_REPO, TEST_USER_NAME


# Testing Repo Network
def test_repo_network():
    '''
    Test the repository network data loader.
    '''
    # Create a data loader instance for repository network
    repo_network_dataloader = RepoNetworkRepoDataloader()
    # Load repository network data for the test organization and repository
    success_data = repo_network_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load repository network data for a non-existing repository
    fail_data = repo_network_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success

    # Create a data loader instance for user's repository network
    repo_network_user_dataloader = RepoNetworkUserDataloader()
    # Load repository network data for the test user
    success_data = repo_network_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    # Load repository network data for a non-existing user
    fail_data = repo_network_user_dataloader.load("non-exist-user")
    assert not fail_data.is_success


# Testing Developer Network
def test_developer_network():
    '''
    Test the developer network data loader.
    '''
    # Create a data loader instance for developer network
    developer_network_dataloader = DeveloperNetworkRepoDataloader()
    # Load developer network data for the test organization and repository
    success_data = developer_network_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    # Load developer network data for a non-existing repository
    fail_data = developer_network_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success

    # Create a data loader instance for user's developer network
    developer_network_user_dataloader = DeveloperNetworkUserDataloader()
    # Load developer network data for the test user
    success_data = developer_network_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    # Load developer network data for a non-existing user
    fail_data = developer_network_user_dataloader.load("non-exist-user")
    assert not fail_data.is_success


# Testing Project OpenRank Network
def test_project_openrank_network():
    '''
    Test the project's OpenRank network for a specific month.
    '''
    # Create a data loader instance for project's OpenRank network
    project_openrank_network_dataloader = (
        ProjectOpenRankNetworkRepoDataloader()
    )
    # Load project's OpenRank network data for the test organization, repository, and month
    success_data = project_openrank_network_dataloader.load(
        TEST_ORG, TEST_REPO, "2022-12"
    )
    assert success_data.is_success

    # Load project's OpenRank network data for a non-existing repository and month
    fail_data = project_openrank_network_dataloader.load(
        TEST_ORG, "non-exist-repo", "2022-12"
    )
    assert not fail_data.is_success

