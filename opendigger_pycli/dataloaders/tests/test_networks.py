from opendigger_pycli.dataloaders.networks import (
    DeveloperNetworkRepoDataloader,
    DeveloperNetworkUserDataloader,
    ProjectOpenRankNetworkRepoDataloader,
    RepoNetworkRepoDataloader,
    RepoNetworkUserDataloader,
)

from . import TEST_ORG, TEST_REPO, TEST_USER_NAME


def test_repo_network():
    repo_network_dataloader = RepoNetworkRepoDataloader()
    success_data = repo_network_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = repo_network_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success

    repo_network_user_dataloader = RepoNetworkUserDataloader()
    success_data = repo_network_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    fail_data = repo_network_user_dataloader.load("non-exist-user")
    assert not fail_data.is_success


def test_developer_network():
    developer_network_dataloader = DeveloperNetworkRepoDataloader()
    success_data = developer_network_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = developer_network_dataloader.load(TEST_ORG, "non-exist-repo")
    assert not fail_data.is_success

    developer_network_user_dataloader = DeveloperNetworkUserDataloader()
    success_data = developer_network_user_dataloader.load(TEST_USER_NAME)
    assert success_data.is_success

    fail_data = developer_network_user_dataloader.load("non-exist-user")
    assert not fail_data.is_success


def test_project_openrank_network():
    project_openrank_network_dataloader = ProjectOpenRankNetworkRepoDataloader()
    success_data = project_openrank_network_dataloader.load(
        TEST_ORG, TEST_REPO, [(2022, 12)]
    )
    assert success_data.is_success

    fail_data = project_openrank_network_dataloader.load(
        TEST_ORG, "non-exist-repo", [(2022, 12)]
    )
    assert not fail_data.data.value[0].value
