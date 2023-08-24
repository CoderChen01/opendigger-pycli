import typing as t

from rich.table import Table

from opendigger_pycli.utils.git_api import (
    REPO_INFO_DICT,
    get_repo_info,
    get_user_info,
)
from . import CONSOLE


def print_user_info(usernames: t.List[str]):
    pass

# 定义一个函数，接受一个仓库列表和可选的 GitHub PAT 作为参数
def print_repo_info(
    repos: t.List[t.Tuple[str, str]], github_pat: t.Optional[str] = None
):
    # 创建一个 Table 对象用于显示表格
    table = Table(show_lines=True)
    # 添加表头列
    # 设置列名和溢出处理方式
    table.add_column("Repository", overflow="fold")
    table.add_column("Repository URL", overflow="fold")

    name_map = {}
    # 遍历 REPO_INFO_DICT 字典的字段名，将其转换为标题形式并添加到表头
    for key in REPO_INFO_DICT.__annotations__.keys():
        name = " ".join(key.split("_")).title()  # 将字段名转换为标题形式
        name_map[name] = key  # 将标题名与字段名建立映射关系
        table.add_column(name, overflow="fold")  # 添加列到表格

    # 遍历传入的仓库列表
    for org_name, repo_name in repos:
        repo_info = get_repo_info(org_name, repo_name, github_pat)  # 获取仓库信息
        repo_info = None
        if repo_info is None:
            # 如果未获取到仓库信息，打印失败信息，添加一行到表格
            CONSOLE.print(
                f"[red]fail to request repo [green]{org_name}/{repo_name}[/] [red]info![/]"
            )
            table.add_row(
                f"{org_name}/{repo_name}",
                f"https://www.github.com/{org_name}/{repo_name}",
                *["null" for _ in range(len(name_map))],  # 用 "null" 填充缺失的列数据
            )
        else:
            # 如果获取到了仓库信息，添加一行到表格，填充各个字段的数据
            table.add_row(
                f"{org_name}/{repo_name}",
                f"https://www.github.com/{org_name}/{repo_name}",
                *[str(repo_info[name_map[key]]) for key in name_map],  # 使用字段名从 repo_info 中获取数据
            )
    # 使用 CONSOLE 打印表格，使用 soft_wrap 处理长文本
    CONSOLE.print(table, soft_wrap=True)
