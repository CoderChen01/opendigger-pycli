import typing as t

import requests

# 仓库信息（仓库地址url、是否fork、创建时间和更新时间）
REPO_INFO_DICT = t.TypedDict(
    "repo_info",
    owner_url=str,
    is_fork=str,
    created_at=str,
    updated_at=str,
)
# 用户信息（用户名、用户姓名和邮箱地址）
USER_INFO_DICT = t.TypedDict("user_info", username=str, name=str, email=str)


def get_repo_info(
    org_name: str, repo_name: str, github_pat: t.Optional[str] = None
) -> t.Optional[REPO_INFO_DICT]:
    """
    Get repo info from GitHub API

    Args:
        org_name (str): 组织（或用户）名称。
        repo_name (str): 仓库名称。
        github_pat (str, 可选): GitHub 的个人访问令牌（Personal Access Token）

    return:
        t.Optional[USER_INFO_DICT]: 符合 USER_INFO_DICT 类型的用户信息字典，或者返回 None 如果没有找到相关信息。
    """
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"

    if github_pat is not None:
        response = requests.get(
            url,
            headers={"Authorization": f"token {github_pat}"},
        )
        # 发起带有访问令牌的 API 请求
    else:
        response = requests.get(url)  # 发起无令牌的 API 请求

    if response.status_code != 200:
        return None
        # 如果响应状态码不是 200（成功），则返回 None

    data = response.json()  # 解析响应数据为 JSON 格式

    # 返回仓库信息字典，符合 REPO_INFO_DICT 类型
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
