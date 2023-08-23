import requests


def exist_gh_repo(org_name: str, repo_name: str) -> bool:
    """
    Check if a repo exists on GitHub
    """
    url = f"https://github.com/{org_name}/{repo_name}"
    resp = requests.get(url)
    return resp.status_code == 200


def exist_gh_user(username: str) -> bool:
    """
    Check if a user exists on GitHub
    """
    url = f"https://github.com/{username}"
    resp = requests.get(url)
    return resp.status_code == 200
