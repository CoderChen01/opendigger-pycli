from opendigger_pycli.datatypes import OpenRankData, ActivityData, AttentionData
from .base import (
    BaseRepoDataLoader,
    BaseUserDataLoader,
    DataLoaderState,
    register_dataloader,
    get_repo_data,
    get_developer_data,
    load_base_data,
    load_non_trival_metric_data,
    load_name_and_value,
)


@register_dataloader
class OpenRankRepoDataloader(BaseRepoDataLoader[OpenRankData]):
    name = "openrank"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataLoaderState[OpenRankData]:
        data = get_repo_data(org, repo, OpenRankData.name)
        if data is None:
            return DataLoaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataLoaderState(
            is_success=True,
            data=OpenRankData(value=load_base_data(data, float)),
            desc="",
        )


@register_dataloader
class ActivityRepoDataloader(BaseRepoDataLoader[ActivityData]):
    name = "activity"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataLoaderState[ActivityData]:
        data = get_repo_data(org, repo, ActivityData.name)
        if data is None:
            return DataLoaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataLoaderState(
            is_success=True,
            data=ActivityData(
                value=load_base_data(data, load_name_and_value),
            ),
            desc="",
        )


@register_dataloader
class AttentionRepoDataloader(BaseRepoDataLoader[AttentionData]):
    name = "attention"
    metric_type = "index"

    def load(self, org: str, repo: str) -> DataLoaderState[AttentionData]:
        data = get_repo_data(org, repo, AttentionData.name)
        if data is None:
            return DataLoaderState(
                is_success=False,
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataLoaderState(
            is_success=True,
            data=AttentionData(
                value=load_base_data(data, int),
            ),
            desc="",
        )
