import typing as t

import requests

REPO_INFO_DICT = t.TypedDict(
    "repo_info",
    repository=str,
    repository_url=str,
    owner_url=str,
    is_fork=str,
    created_at=str,
    updated_at=str,
)
USER_INFO_DICT = t.TypedDict(
    "user_info",
    username=str,
    name=str,
    email=str,
    github_homepage_url=str,
    created_at=str,
    updated_at=str,
)


def get_repo_info(
    org_name: str, repo_name: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, REPO_INFO_DICT]:
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
        return False, REPO_INFO_DICT(
            repository=f"{org_name}/{repo_name}",
            repository_url=f"https://www.github.com/{org_name}/{repo_name}",
            owner_url="null",
            is_fork="null",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, REPO_INFO_DICT(
        repository=f"{org_name}/{repo_name}",
        repository_url=f"https://www.github.com/{org_name}/{repo_name}",
        owner_url=data["owner"]["html_url"],
        is_fork=str(data["fork"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def get_user_info(
    username: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, USER_INFO_DICT]:
    url = f"https://api.github.com/users/{username}"

    if github_pat is not None:
        response = requests.get(url, headers={"Authorization": f"token {github_pat}"})
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return False, USER_INFO_DICT(
            username=username,
            name="null",
            email="null",
            github_homepage_url=f"https://www.github.com/{username}",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, USER_INFO_DICT(
        username=username,
        name=data["name"],
        email=data["email"] if data["email"] is not None else "null",
        github_homepage_url=data["html_url"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
