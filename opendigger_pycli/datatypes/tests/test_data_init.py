from opendigger_pycli.datatypes.indicators.base import AvgDataType, BaseData
from opendigger_pycli.datatypes.indicators.indices import OpenRankData
from opendigger_pycli.datatypes.indicators.metrics import IssueResponseTimeData


def test_init_data():
    data = OpenRankData(value=[BaseData(year=2023, month=1, value=1)])
    assert data is not None
    issue_response_time = IssueResponseTimeData(
        value={
            "avg": [AvgDataType(year=2023, month=1, value=1.0)],
            "levels": [BaseData(year=2023, month=1, value=[1])],
            "quantile0": [BaseData(year=2023, month=1, value=1)],
            "quantile1": [BaseData(year=2023, month=1, value=1)],
            "quantile2": [BaseData(year=2023, month=1, value=1.0)],
            "quantile3": [BaseData(year=2023, month=1, value=1.0)],
            "quantile4": [BaseData(year=2023, month=1, value=1.0)],
        }
    )
    assert issue_response_time is not None
