from opendigger_pycli.dataloaders import (
    OpenRankRepoDataloader,
    OpenRankUserDataLoader,
    ProjectOpenRankNetworkRepoDataloader,
)
from opendigger_pycli.datatypes import DataloaderProto


def test_dataloader_proto_check():
    assert isinstance(ProjectOpenRankNetworkRepoDataloader(), DataloaderProto)
    assert isinstance(OpenRankRepoDataloader(), DataloaderProto)
    assert isinstance(OpenRankUserDataLoader(), DataloaderProto)
