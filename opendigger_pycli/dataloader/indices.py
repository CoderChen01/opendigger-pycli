from opendigger_pycli.datatypes import (
    ActivityData,
    AttentionData,
    OpenRankData,
)

from .base import (
    BaseRepoDataloader,
    BaseUserDataloader,
    DataloaderState,
    get_developer_data,
    get_repo_data,
    load_base_data,
    load_name_and_value,
    register_dataloader,
)


@register_dataloader
class OpenRankRepoDataloader(BaseRepoDataloader[OpenRankData]):
    '''
    Data loader for the OpenRank repository metric.
    '''
    name = "openrank"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataloaderState[OpenRankData]:
        '''
        Load OpenRank repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[OpenRankData]: The state of the data loading operation.
        '''
        data = get_repo_data(org, repo, OpenRankData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=OpenRankData(value=load_base_data(data, float)),
            desc="",
        )


@register_dataloader
class ActivityRepoDataloader(BaseRepoDataloader[ActivityData]):
    '''
    Data loader for the Activity repository metric.
    '''
    name = "activity"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataloaderState[ActivityData]:
        '''
        Load Activity repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[ActivityData]: The state of the data loading operation.
        '''
        data = get_repo_data(org, repo, ActivityData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=ActivityData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )



@register_dataloader
class AttentionRepoDataloader(BaseRepoDataloader[AttentionData]):
    '''
    Data loader for the Attention repository metric.
    '''
    name = "attention"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataloaderState[AttentionData]:
        '''
        Load Attention repository data for the given organization and repository.

        Args:
            org (str): The organization name.
            repo (str): The repository name.

        Returns:
            DataloaderState[AttentionData]: The state of the data loading operation.
        '''
        data = get_repo_data(org, repo, AttentionData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=AttentionData(
                value=load_base_data(data, int),
            ),
            desc="",
        )



@register_dataloader
class OpenRankUserDataLoader(BaseUserDataloader[OpenRankData]):
    '''
    Data loader for OpenRank user data.
    '''
    name = "openrank"
    metric_type = "index"

    def load(self, username: str) -> DataloaderState[OpenRankData]:
        '''
        Load OpenRank user data for the given username.

        Args:
            username (str): The username of the user.

        Returns:
            DataloaderState[OpenRankData]: The state of the data loading operation.
        '''
        data = get_developer_data(username, OpenRankData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=OpenRankData(value=load_base_data(data, float)),
            desc="",
        )


@register_dataloader
class ActivityUserDataLoader(BaseUserDataloader[ActivityData]):
    '''
    Data loader for Activity user data.
    '''
    name = "activity"
    metric_type = "index"

    def load(self, username: str) -> DataloaderState[ActivityData]:
        '''
        Load Activity user data for the given username.

        Args:
            username (str): The username of the user.

        Returns:
            DataloaderState[ActivityData]: The state of the data loading operation.
        '''
        data = get_developer_data(username, ActivityData.name)
        if data is None:
            return DataloaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderState(
            is_success=True,
            data=ActivityData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )
