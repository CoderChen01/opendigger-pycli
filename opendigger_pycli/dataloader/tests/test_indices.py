from opendigger_pycli.dataloader.indices import (
    ActivityRepoDataloader,
    OpenRankRepoDataloader,
    AttentionRepoDataloader,
)

TEST_ORG = "X-lab2017"
TEST_REPO = "open-digger"


def test_openrank():
    openrank_dataloader = OpenRankRepoDataloader()
    success_data = openrank_dataloader.load(TEST_ORG, TEST_REPO)
    assert success_data.is_success

    fail_data = openrank_dataloader.load(TEST_ORG, "not-exist-repo")
    assert not fail_data.is_success


def test_activity():
    pass


def test_attention():
    pass
