import json
import typing as t
from dataclasses import asdict

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        BaseNetworkData,
        NameAndValue,
        NonTrivalNetworkInciatorData,
        NonTrivialIndicatorData,
        TrivialIndicatorData,
        TrivialNetworkIndicatorData,
    )


def export_trivial_network_to_json(
    indicator_data: "TrivialNetworkIndicatorData",
) -> t.Dict[str, t.Any]:
    result = {}
    warmup = getattr(indicator_data.value, "nodes")[0]
    if hasattr(warmup, "tuple"):
        nodes: t.List[t.Tuple[str, float]] = []
        edges: t.List[t.Tuple[str, str, float]] = []
        base_network_data = t.cast("TrivialNetworkIndicatorData", indicator_data).value
        for node in base_network_data.nodes:
            nodes.append(node.tuple)
        for edge in base_network_data.edges:
            edges.append(edge.tuple)
        result = {"nodes": nodes, "edges": edges}
    else:
        result = asdict(indicator_data)

    return result


def export_non_trivial_indicator_to_json(
    indicator_data: "NonTrivialIndicatorData",
) -> t.Dict[str, t.Any]:
    result: t.Dict[str, t.Dict[str, t.Any]] = {}
    indicator_data = t.cast("NonTrivialIndicatorData", indicator_data)
    for key, values in indicator_data.value.items():
        result[key] = {}
        for base_data in values:  # type: ignore
            value = t.cast("BaseData", base_data)
            sub_key = (
                f"{value.year}-{value.month:02}-raw"
                if value.is_raw
                else f"{value.year}-{value.month:02}"
            )
            result[key][sub_key] = value.value  # type: ignore
    return result


def export_indicator_to_json(
    indicator_data: t.Union[
        "TrivialIndicatorData",
        "NonTrivialIndicatorData",
        "TrivialNetworkIndicatorData",
        "NonTrivalNetworkInciatorData",
    ],
) -> t.Dict[str, t.Any]:
    if hasattr(indicator_data.value, "nodes"):
        indicator_data = t.cast("TrivialNetworkIndicatorData", indicator_data)
        return export_trivial_network_to_json(indicator_data)

    if isinstance(indicator_data.value, dict):
        indicator_data = t.cast("NonTrivialIndicatorData", indicator_data)
        return export_non_trivial_indicator_to_json(indicator_data)

    values = t.cast("t.List", indicator_data.value)
    warmup = values[0]
    result: t.Dict[str, t.Any] = {}
    if hasattr(warmup.value, "nodes") or warmup.value is None:
        base_data_list = t.cast("t.List[BaseData[BaseNetworkData]]", values)
        for base_data in base_data_list:
            key = (
                f"{base_data.year}-{base_data.month:02}-raw"
                if base_data.is_raw
                else f"{base_data.year}-{base_data.month:02}"
            )
            result[key] = asdict(base_data.value) if base_data.value else None
    else:
        values = t.cast("t.List[BaseData]", values)
        for value in values:
            key = (
                f"{value.year}-{value.month:02}-raw"
                if value.is_raw
                else f"{value.year}-{value.month:02}"
            )
            if isinstance(value.value, list) and hasattr(value.value[0], "name"):
                value.value = t.cast("t.List[NameAndValue]", value.value)
                result[key] = [v.tuple for v in value.value]
            else:
                result[key] = value.value

    return result
