from opendigger_pycli.datatypes import DataloaderProto
from opendigger_pycli.dataloader import (
    ProjectOpenRankNetworkRepoDataloader,
    OpenRankRepoDataloader,
    OpenRankUserDataLoader,
)


def test_dataloader_proto_check():
    assert isinstance(ProjectOpenRankNetworkRepoDataloader(), DataloaderProto)
    assert isinstance(OpenRankRepoDataloader(), DataloaderProto)
    assert isinstance(OpenRankUserDataLoader(), DataloaderProto)
