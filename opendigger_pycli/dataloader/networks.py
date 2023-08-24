from opendigger_pycli.datatypes import (
    BaseData,
    DeveloperNetworkData,
    ProjectOpenRankNetworkData,
    RepoNetworkData,
)

from .base import (
    BaseOpenRankNetworkDataloader,
    BaseRepoDataloader,
    BaseUserDataloader,
    DataloaderState,
    register_dataloader,
)
from .utils import (
    get_developer_data,
    get_repo_data,
    load_network_data,
    load_openrank_network_data,
)


@register_dataloader
class DeveloperNetworkRepoDataloader(BaseRepoDataloader):
    name = "developer_network"
    metric_type = "network"
    introducer = "X-lab"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[DeveloperNetworkData]:
        data = get_repo_data(org, repo, DeveloperNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=DeveloperNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class RepoNetworkRepoDataloader(BaseRepoDataloader):
    name = "repo_network"
    metric_type = "network"
    introducer = "X-lab"

    def load(self, org: str, repo: str) -> DataloaderState[RepoNetworkData]:
        data = get_repo_data(org, repo, RepoNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=RepoNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class ProjectOpenRankNetworkRepoDataloader(BaseOpenRankNetworkDataloader):
    name = "project_openrank_detail"
    metric_type = "network"
    type = "repo"
    introducer = "X-lab"

    def load(
        self, org: str, repo: str, date: str
    ) -> DataloaderState[ProjectOpenRankNetworkData]:
        data = get_repo_data(org, repo, ProjectOpenRankNetworkData.name, date)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        year, month = date.split("-")[:2]
        return DataloaderState(
            is_success=True,
            data=ProjectOpenRankNetworkData(
                value=BaseData(
                    year=int(year),
                    month=int(month),
                    value=load_openrank_network_data(data),
                )
            ),
            desc="",
        )


@register_dataloader
class DeveloperNetworkUserDataloader(BaseUserDataloader):
    name = "developer_network"
    metric_type = "network"
    introducer = "X-lab"

    def load(self, username: str) -> DataloaderState[DeveloperNetworkData]:
        data = get_developer_data(username, DeveloperNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=DeveloperNetworkData(value=load_network_data(data)),
            desc="",
        )


@register_dataloader
class RepoNetworkUserDataloader(BaseUserDataloader):
    name = "repo_network"
    metric_type = "network"
    introducer = "X-lab"

    def load(self, username: str) -> DataloaderState[RepoNetworkData]:
        data = get_developer_data(username, RepoNetworkData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=RepoNetworkData(value=load_network_data(data)),
            desc="",
        )
