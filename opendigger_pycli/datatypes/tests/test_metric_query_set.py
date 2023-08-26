from opendigger_pycli.datatypes import MetricQuery


def test_metric_query_set():
    q1 = MetricQuery(
        months=frozenset([1, 2, 3]),
        years=frozenset([2019, 2020]),
        year_months=frozenset([(2019, 1), (2020, 2)]),
    )
    q2 = MetricQuery(
        months=frozenset([1, 2, 3]),
        years=frozenset([2019, 2020]),
        year_months=frozenset([(2019, 1), (2020, 2)]),
    )
    q3 = None

    assert set([q1, q2, q3]) == set([q1, q3])
