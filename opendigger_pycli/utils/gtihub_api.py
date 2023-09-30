import typing as t

import requests

_GITHUB_API_BASE_URL = "https://api.github.com"


class RepoInfoType(t.TypedDict):
    repository: str
    repository_url: str
    owner_url: str
    is_fork: str
    created_at: str
    updated_at: str


class UserInfoType(t.TypedDict):
    username: str
    name: str
    email: str
    github_homepage_url: str
    created_at: str
    updated_at: str


class IssueInfoType(t.TypedDict):
    org_name: str
    repo_name: str
    issue_number: int
    issue_title: str
    issue_api_url: str
    issue_html_url: str


class IssueCommentInfoType(t.TypedDict):
    issue_comment_api_url: str
    body: str


def get_repo_info(
    org_name: str, repo_name: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, RepoInfoType]:
    """
    Get repo info from GitHub API
    """
    url = f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}"

    if github_pat is not None:
        response = requests.get(
            url,
            headers={"Authorization": f"token {github_pat}"},
        )
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return False, RepoInfoType(
            repository=f"{org_name}/{repo_name}",
            repository_url=f"https://www.github.com/{org_name}/{repo_name}",
            owner_url="null",
            is_fork="null",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, RepoInfoType(
        repository=f"{org_name}/{repo_name}",
        repository_url=f"https://www.github.com/{org_name}/{repo_name}",
        owner_url=data["owner"]["html_url"],
        is_fork=str(data["fork"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def get_user_info(
    username: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, UserInfoType]:
    url = f"{_GITHUB_API_BASE_URL}/users/{username}"

    if github_pat is not None:
        response = requests.get(url, headers={"Authorization": f"token {github_pat}"})
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return False, UserInfoType(
            username=username,
            name="null",
            email="null",
            github_homepage_url=f"https://www.github.com/{username}",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, UserInfoType(
        username=username,
        name=data["name"],
        email=data["email"] if data["email"] is not None else "null",
        github_homepage_url=data["html_url"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def create_issue(
    org_name: str,
    repo_name: str,
    github_pat: str,
    title: str,
    body: t.Optional[str] = None,
    labels: t.Optional[t.List[str]] = None,
    assignees: t.Optional[t.List[str]] = None,
) -> t.Tuple[bool, t.Optional[IssueInfoType]]:
    url: str = f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}/issues"

    data: t.Dict[str, t.Union[str, t.List[str], int]] = {
        "title": title,
    }

    if labels:
        data["labels"] = labels
    if assignees:
        data["assignees"] = assignees
    if body:
        data["body"] = body

    response = requests.post(
        url=url,
        headers={"Authorization": f"token {github_pat}"},
        json=data,
    )

    if response.status_code == 201:
        dat = response.json()
        return True, IssueInfoType(
            org_name=org_name,
            repo_name=repo_name,
            issue_number=dat["number"],
            issue_title=dat["title"],
            issue_api_url=dat["url"],
            issue_html_url=dat["html_url"],
        )

    return False, None


def create_issue_comment(issue_api_url: str, body: str, github_pat: str) -> bool:
    response = requests.post(
        url=f"{issue_api_url}/comments",
        json={"body": body},
        headers={"Authorization": f"token {github_pat}"},
    )

    return response.status_code == 201


def create_issue_comment_reactions(
    issue_cooment_api_url: str,
    content: t.Literal[
        "+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"
    ],
    github_pat: str,
) -> bool:
    url = f"{issue_cooment_api_url}/reactions"

    response = requests.post(
        url=url,
        json={"content": content},
        headers={"Authorization": f"token {github_pat}"},
    )

    return response.status_code == 200


def get_issue_comments(
    issue_api_url: str, github_pat: str
) -> t.Tuple[bool, t.List[IssueCommentInfoType]]:
    response = requests.get(
        f"{issue_api_url}/comments", headers={"Authorization": f"token {github_pat}"}
    )

    if response.status_code != 200:
        return False, []

    body_datum = []
    datum = response.json()
    for dat in datum:
        body_datum.append(
            IssueCommentInfoType(
                body=dat["body"],
                issue_comment_api_url=f"{issue_api_url.rsplit('/', 1)[0]}/comments/{dat['id']}",
            )
        )

    return True, body_datum


def get_issue_comment_api_url(
    org_name: str, repo_name: str, issue_number: int, comment_number: int
) -> str:
    return f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}/issues/{issue_number}/comments/{comment_number}"


def search_issue_title(
    org_name: str,
    repo_name: str,
    title: str,
    labels: t.Optional[t.List[str]],
    github_pat: str,
) -> t.Tuple[bool, t.Optional[t.List[IssueInfoType]]]:
    url = f"{_GITHUB_API_BASE_URL}/search/issues"

    query_str = f"{title} repo:{org_name}/{repo_name} is:issue"

    if labels is None:
        labels = []
    for label in labels:
        query_str += f" label:{label}"

    response = requests.get(
        url=url,
        params={"q": query_str},
        headers={"Authorization": f"token {github_pat}"},
    )

    if response.status_code != 200:
        return False, None

    datum = response.json()

    issue_infos = []
    for dat in datum["items"]:
        if dat["title"] != title:
            continue
        issue_infos.append(
            IssueInfoType(
                org_name=org_name,
                repo_name=repo_name,
                issue_number=dat["number"],
                issue_title=dat["title"],
                issue_api_url=dat["url"],
                issue_html_url=dat["html_url"],
            )
        )

    if not issue_infos:
        return False, None

    return True, issue_infos
