import typing as t

from opendigger_pycli.datatypes import (
    ActivityData,
    AttentionData,
    DataloaderResult,
    OpenRankData,
)

from .base import BaseRepoDataloader, BaseUserDataloader, register_dataloader
from .utils import (
    get_developer_data,
    get_repo_data,
    load_base_data,
    load_name_and_value,
)

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.dataloader import DataloaderProto


@register_dataloader
class OpenRankRepoDataloader(BaseRepoDataloader):
    name = "openrank"
    indicator_type = "index"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/openrank.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[OpenRankData]:
        data = get_repo_data(org, repo, OpenRankData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=OpenRankData(value=load_base_data(data, float)),
            desc="",
        )


@register_dataloader
class ActivityRepoDataloader(BaseRepoDataloader):
    name = "activity"
    indicator_type = "index"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/activity.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[ActivityData]:
        data = get_repo_data(org, repo, ActivityData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActivityData(
                value=load_base_data(data, float),
            ),
            desc="",
        )


@register_dataloader
class AttentionRepoDataloader(BaseRepoDataloader):
    name = "attention"
    indicator_type = "index"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/attention.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[AttentionData]:
        data = get_repo_data(org, repo, AttentionData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=AttentionData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class OpenRankUserDataLoader(BaseUserDataloader):
    name = "openrank"
    indicator_type = "index"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/frank-zsy/openrank.json"

    def load(self, username: str) -> DataloaderResult[OpenRankData]:
        data = get_developer_data(username, OpenRankData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=OpenRankData(value=load_base_data(data, float)),
            desc="",
        )


@register_dataloader
class ActivityUserDataLoader(BaseUserDataloader):
    name = "activity"
    indicator_type = "index"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/frank-zsy/activity.json"

    def load(self, username: str) -> DataloaderResult[ActivityData]:
        data = get_developer_data(username, ActivityData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActivityData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )
