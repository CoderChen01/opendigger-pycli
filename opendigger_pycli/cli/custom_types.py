import typing as t

import click
from click import Parameter, Context

from opendigger_pycli.utils.checkers import exist_gh_repo

# 自定义 RepoNameType 类，继承自 click.ParamType
class RepoNameType(click.ParamType):
    name = "repo_name"

    def convert(
        self,
        value: str,
        param: t.Optional[Parameter],
        ctx: t.Optional[Context],
    ) -> t.Tuple[str, str]:
        try:
            org_name, repo_name = value.split("/")  # 将参数按 / 分割成组织名和仓库名
            if not exist_gh_repo(org_name, repo_name):  # 使用 exist_gh_repo 函数检查 GitHub 仓库是否存在，如果不存在，报错
                self.fail(
                    f"{value} repo does not exist, please check https://www.github.com/{org_name}/{repo_name}"
                )
            return org_name, repo_name
        except ValueError:
            self.fail(f"{value} is not a valid repo name")  # 如果分割失败，报错


# 创建一个 REPO_NAME_TYPE 的实例，用于处理参数为组织名/仓库名的输入
REPO_NAME_TYPE = RepoNameType()
