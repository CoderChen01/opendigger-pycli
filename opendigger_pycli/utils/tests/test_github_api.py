import uuid

from opendigger_pycli.utils.gtihub_api import create_issue


def test_create_issue(test_github_pat) -> None:
    assert create_issue(
        github_pat=test_github_pat,
        org_name="CoderChen01",
        repo_name="opendigger-pycli",
        title="test issue" + uuid.uuid4().hex,
        body="test issue body",
        labels=["nodata"],
        assignees=["CoderChen01"],
    )
