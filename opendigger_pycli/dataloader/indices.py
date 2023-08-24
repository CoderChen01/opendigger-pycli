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
    name = "openrank"
    metric_type = "index"
    introducer = "X-lab"

    def load(self, org: str, repo: str) -> DataloaderState[OpenRankData]:
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
    name = "activity"
    metric_type = "index"
    introducer = "X-lab"

    def load(self, org: str, repo: str) -> DataloaderState[ActivityData]:
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
    name = "attention"
    metric_type = "index"
    introducer = "X-lab"

    def load(self, org: str, repo: str) -> DataloaderState[AttentionData]:
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
    name = "openrank"
    metric_type = "index"
    introducer = "X-lab"

    def load(self, username: str) -> DataloaderState[OpenRankData]:
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
    name = "activity"
    metric_type = "index"
    introducer = "X-lab"

    def load(self, username: str) -> DataloaderState[ActivityData]:
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
