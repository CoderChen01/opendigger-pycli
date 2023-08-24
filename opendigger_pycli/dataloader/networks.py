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
    get_developer_data,
    get_repo_data,
    load_network_data,
    load_openrank_network_data,
    register_dataloader,
)


@register_dataloader
class DeveloperNetworkRepoDataloader(BaseRepoDataloader[DeveloperNetworkData]):
    '''
    Data loader for DeveloperNetwork repository data.
    '''
    name = "developer_network"
    metric_type = "network"

    def load(
        self, org: str, repo: str
    ) -> DataloaderState[DeveloperNetworkData]:
        '''
        Load DeveloperNetwork repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[DeveloperNetworkData]: The state of the data loading operation.
        '''
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
class RepoNetworkRepoDataloader(BaseRepoDataloader[RepoNetworkData]):
    '''
    Data loader for RepoNetwork repository data.
    '''
    name = "repo_network"
    metric_type = "network"

    def load(self, org: str, repo: str) -> DataloaderState[RepoNetworkData]:
        '''
        Load RepoNetwork repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[RepoNetworkData]: The state of the data loading operation.
        '''
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
class ProjectOpenRankNetworkRepoDataloader(
    BaseOpenRankNetworkDataloader[ProjectOpenRankNetworkData]
):
    '''
    Data loader for ProjectOpenRankNetwork repository data.
    '''
    name = "project_openrank_detail"
    metric_type = "network"

    def load(
        self, org: str, repo: str, date: str
    ) -> DataloaderState[ProjectOpenRankNetworkData]:
        '''
        Load ProjectOpenRankNetwork repository data for the given organization, repository, and date.

        Args:
            org (str): The organization name.
            repo (str): The repository name.
            date (str): The date in "YYYY-MM" format.

        Returns:
            DataloaderState[ProjectOpenRankNetworkData]: The state of the data loading operation.
        '''
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
class DeveloperNetworkUserDataloader(BaseUserDataloader[DeveloperNetworkData]):
    '''
    Data loader for DeveloperNetwork user data.
    '''
    name = "developer_network"
    metric_type = "network"

    def load(self, username: str) -> DataloaderState[DeveloperNetworkData]:
        '''
        Load DeveloperNetwork user data for the given username.

        Args:
            username (str): The username of the developer.

        Returns:
            DataloaderState[DeveloperNetworkData]: The state of the data loading operation.
        '''
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
class RepoNetworkUserDataloader(BaseUserDataloader[RepoNetworkData]):
    '''
    Data loader for RepoNetwork user data.
    '''
    name = "repo_network"
    metric_type = "network"

    def load(self, username: str) -> DataloaderState[RepoNetworkData]:
        '''
        Load RepoNetwork user data for the given username.

        Args:
            username (str): The username of the developer.

        Returns:
            DataloaderState[RepoNetworkData]: The state of the data loading operation.
        '''
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

