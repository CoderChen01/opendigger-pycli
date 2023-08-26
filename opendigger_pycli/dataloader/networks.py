import typing as t

from opendigger_pycli.datatypes import (
    BaseData,
    DeveloperNetworkData,
    ProjectOpenRankNetworkData,
    RepoNetworkData,
    DataloaderState,
)

from .base import (
    BaseOpenRankNetworkDataloader,
    BaseRepoDataloader,
    BaseUserDataloader,
    register_dataloader,
)
from .utils import (
    get_developer_data,
    get_repo_data,
    load_network_data,
    load_openrank_network_data,
)

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.dataloader import DataloaderProto


@register_dataloader
class DeveloperNetworkRepoDataloader(BaseRepoDataloader):
    name = "developer_network"
    metric_type = "network"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/developer_network.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[DeveloperNetworkData]:
        data = get_repo_data(org, repo, DeveloperNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=DeveloperNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class RepoNetworkRepoDataloader(BaseRepoDataloader):
    name = "repo_network"
    metric_type = "network"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/repo_network.json"

    def load(self, org: str, repo: str) -> DataloaderState[RepoNetworkData]:
        data = get_repo_data(org, repo, RepoNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=RepoNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class ProjectOpenRankNetworkRepoDataloader(BaseOpenRankNetworkDataloader):
    name = "project_openrank_detail"
    metric_type = "network"
    type = "repo"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/project_openrank_detail/2022-12.json"
    pass_date = True

    def load(
        self, org: str, repo: str, dates: t.List[t.Tuple[int, int]]
    ) -> DataloaderState[ProjectOpenRankNetworkData]:
        values = []
        for date in dates:
            data = get_repo_data(
                org, repo, ProjectOpenRankNetworkData.name, date
            )
            if data is None:
                return DataloaderState(
                    is_success=False,
                    dataloader=t.cast("DataloaderProto", self),
                    data=None,
                    desc="Cannot find data for this indicator",
                )
            year, month = date
            values.append(
                BaseData(
                    year=int(year),
                    month=int(month),
                    value=load_openrank_network_data(data),
                )
            )
        return DataloaderState(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ProjectOpenRankNetworkData(value=values),
            desc="",
        )


@register_dataloader
class DeveloperNetworkUserDataloader(BaseUserDataloader):
    name = "developer_network"
    metric_type = "network"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/frank-zsy/developer_network.json"

    def load(self, username: str) -> DataloaderState[DeveloperNetworkData]:
        data = get_developer_data(username, DeveloperNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=DeveloperNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class RepoNetworkUserDataloader(BaseUserDataloader):
    name = "repo_network"
    metric_type = "network"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/frank-zsy/repo_network.json"
    )

    def load(self, username: str) -> DataloaderState[RepoNetworkData]:
        data = get_developer_data(username, RepoNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=RepoNetworkData(value=load_network_data(data)),
            desc="",
        )
