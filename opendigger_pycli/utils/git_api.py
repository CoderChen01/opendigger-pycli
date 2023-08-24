import typing as t

import requests


REPO_INFO_DICT = t.TypedDict(
    "repo_info",
    owner_url=str,
    is_fork=str,
    created_at=str,
    updated_at=str,
)
USER_INFO_DICT = t.TypedDict("user_info", username=str, name=str, email=str)


def get_repo_info(
    org_name: str, repo_name: str, github_pat: t.Optional[str] = None
) -> t.Optional[REPO_INFO_DICT]:
    """
    Get repo info from GitHub API
    """
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"

    if github_pat is not None:
        response = requests.get(
            url,
            headers={"Authorization": f"token {github_pat}"},
        )
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return REPO_INFO_DICT(
        owner_url=data["owner"]["html_url"],
        is_fork=str(data["fork"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def get_user_info(
    username: str, github_pat: t.Optional[str] = None
) -> t.Optional[USER_INFO_DICT]:
    pass
