import math
import typing as t
from functools import partial

from rich.color import blend_rgb
from rich.color_triplet import ColorTriplet
from rich.columns import Columns

from . import CONSOLE

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import BaseData, BaseNetworkData, NameAndValue

DELIM = ","
POSITIVE_TICK = "▇"
NEGTIVE_TICK = "━"
SM_TICK = "|"
HEATMAP_CHAR = "▓"


def print_header_row() -> None:
    CONSOLE.print(f"[red]{NEGTIVE_TICK}[/]" + " " + "Negative Value" + "  ", end="")
    CONSOLE.print(f"[green]{POSITIVE_TICK}[/]" + " " + "Positive Value" + "  ", end="")
    CONSOLE.print("", end="\n\n")


def print_bar_row(
    label: str,
    value: t.Union[int, float],
    num_blocks: t.Union[int, float],
    tail: str = "",
    color: t.Optional[str] = None,
) -> None:
    """A method to print a row for a horizontal graphs.
    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """
    CONSOLE.print(label, end=" ")

    if num_blocks < 1:
        sm_tick = SM_TICK
        if color:
            tick = f"[{color}]{SM_TICK}"
        CONSOLE.print(sm_tick, end="")
    else:
        tick = POSITIVE_TICK if value > 0 else NEGTIVE_TICK
        if color:
            tick = f"[{color}]{tick}"
        for _ in range(int(num_blocks)):
            CONSOLE.print(tick, end="")

    CONSOLE.print(f" {value:.2f}" + tail)


def blocks_num_map(
    values: t.Union[t.List[int], t.List[float]]
) -> t.Callable[[t.Union[int, float]], float]:
    if not values:
        return lambda x: 0
    max_value = max(values)
    min_value = min(values)
    val_range = max_value - min_value
    if val_range == 0:
        val_range = 1
    return lambda x: (abs(x) - min_value) / val_range * CONSOLE.width * 0.8


def print_trivial_base_data_graph(
    base_data_list: t.List["BaseData[t.Union[int, float, t.List[str]]]"],
):
    """Print a graph for a list of BaseData objects.
    The graph is a horizontal graph with a label and a bar.
    """
    print_header_row()

    warm_up_data = base_data_list[0]
    if isinstance(warm_up_data.value, list):
        values = [
            len(data.value)
            for data in t.cast(
                t.List["BaseData[t.List[str]]"],
                base_data_list,
            )
        ]
    else:
        values = t.cast(
            t.List[int],
            [data.value for data in base_data_list],
        )

    neg_blocks_num_map = blocks_num_map([abs(value) for value in values if value < 0])
    positive_blocks_num_map = blocks_num_map([value for value in values if value >= 0])
    for value, data in zip(values, base_data_list):
        label = f"{data.year}-{data.month:02}"
        num_blocks = (
            positive_blocks_num_map(value) if value >= 0 else neg_blocks_num_map(value)
        )
        print_bar_row(
            f"{label}:",
            value,
            num_blocks,
            color="red" if value < 0 else "green",
        )
    CONSOLE.print()
    CONSOLE.print()


def print_non_trivial_base_data_graph(
    base_data_list: t.Union[
        t.List["BaseData[t.List[NameAndValue]]"], t.List["BaseData[t.List[int]]"]
    ],
) -> None:
    """Print a graph for a list of BaseData objects.
    The graph is a horizontal graph with a label and a bar.
    """
    print_header_row()

    warm_up_data = base_data_list[0].value[0]
    if not isinstance(warm_up_data, int):
        base_data_list = t.cast(
            t.List["BaseData[t.List[NameAndValue]]"], base_data_list
        )
        sum_values = [
            sum([nv.value for nv in base_data.value]) for base_data in base_data_list
        ]
        sum_blocks_num_map = blocks_num_map(sum_values)
        values_list = [
            (
                [nv.value for nv in base_data.value],
                [nv.name for nv in base_data.value],
            )
            for base_data in base_data_list
        ]

        CONSOLE.print("# Summary: ", end="\n\n")
        for sum_value, data in zip(sum_values, base_data_list):
            label = f"{data.year}-{data.month:02}"
            print_bar_row(
                f"{label}:",
                sum_value,
                sum_blocks_num_map(sum_value),
                color="green",
            )
        CONSOLE.print()

        CONSOLE.print("# Details: ", end="\n\n")
        for values, data in zip(values_list, base_data_list):
            label = f"{data.year}-{data.month:02}"
            value_map = blocks_num_map(values[0])
            is_first = True
            for value, name in zip(*values):
                if is_first:
                    print_bar_row(
                        f"{label}:",
                        value,
                        value_map(value),
                        color="green",
                        tail=f" ({name})",
                    )
                    is_first = False
                print_bar_row(
                    " " * (len(label) + 1),
                    value,
                    value_map(value),
                    color="green",
                    tail=f" ({name})",
                )
            CONSOLE.print()
    else:
        base_data_list = t.cast(t.List["BaseData[t.List[int]]"], base_data_list)
        all_value_lists = [base_data.value for base_data in base_data_list]
        for value_list, base_data in zip(all_value_lists, base_data_list):
            value_map = blocks_num_map(value_list)
            label = f"{base_data.year}-{base_data.month:02}"
            for i, v in enumerate(value_list):
                if i == 0:
                    print_bar_row(
                        label=f"{label}:",
                        value=v,
                        num_blocks=value_map(v),
                        color="green",
                        tail=f" (Index {i})",
                    )
                else:
                    print_bar_row(
                        label=" " * (len(label) + 1),
                        value=v,
                        num_blocks=value_map(v),
                        color="green",
                        tail=f" (Index {i})",
                    )
            CONSOLE.print()

    CONSOLE.print()
    CONSOLE.print()


def get_base_data_heatmap_data(
    base_data_list: t.List["BaseData[t.List[int]]"],
):
    # Assuming data is provided as a dictionary, sum up all the working hours
    values = [sum(x) for x in zip(*[data.value for data in base_data_list])]

    # Uncomment this line if you want to use log to smooth the data
    # values = [math.log(v + 1) for v in values]

    # Normalize the summed values
    # max_value = max(values)
    # values = [math.ceil(v * 10 / max_value) for v in values]
    result = [[0] * 24 for _ in range(7)]
    for d in range(7):
        for h in range(24):
            result[d][h] = values[d * 24 + h]

    return result


def print_heatmap(data: t.List[t.List[t.Union[int, float]]], *args, **kwargs):
    color = kwargs.pop("color", "red")
    row_labels = kwargs.pop("row_labels", None)
    col_labels = kwargs.pop("col_labels", None)

    max_val = max(map(max, data))  # type: ignore
    min_val = min(map(min, data))  # type: ignore

    # Get the width of the terminal
    console_width = CONSOLE.width

    # Computes the width of the row and column labels (numbers start at 1)
    row_label_width = len(str(len(data)))
    col_label_width = len(str(len(data[0])))

    transpose_needed = (col_label_width + 1) * len(
        data[0]
    ) + row_label_width + 3 > console_width

    # define color gradient
    def get_color(val):
        linear_ratio = (val - min_val) / (max_val - min_val)
        enhanced_ratio = linear_ratio**0.5
        return blend_rgb(
            ColorTriplet(0, 0, 255), ColorTriplet(255, 0, 0), enhanced_ratio
        )

    # When the width is exceeded, change the strategy to use column to print directly
    if transpose_needed:
        items = []
        for row_idx, row in enumerate(data, 1):
            for col_idx, val in enumerate(row, 1):
                color = get_color(val)
                item = f"[{color.hex}]Row({row_idx})-Col({col_idx})-Value({val:.2f})[/]"
                items.append(item)
        columns = Columns(items, equal=True, padding=1)
        CONSOLE.print(columns)
        CONSOLE.print()
    else:
        # Print data and character heatmaps
        for idx, row in enumerate(data, 1):  # Start sequence number is 1
            line = f"{idx:{row_label_width}} | "
            for val in row:
                color = get_color(val)
                line += f"[{color.hex}]{HEATMAP_CHAR * (col_label_width + 1)}[/]"
            CONSOLE.print(line)

        # Print the separator line below the row labels
        header_spacing = " " * (row_label_width + 2)  # 2 for '| '
        CONSOLE.print(header_spacing + "-" * ((col_label_width + 1) * len(data[0])))

        # print column label numbers
        col_numbers = "".join(
            [f"{i+1:{col_label_width + 1}}" for i in range(len(data[0]))]
        )  # start from 1
        CONSOLE.print(header_spacing + col_numbers, end="\n\n")

    # If a column label is provided, print the correspondence between the serial number and the label
    if col_labels:
        name, labels = col_labels
        CONSOLE.print(f"Colunm Labels Denoting [green]{name}[/] Data:")
        labels = [f"Col {i+1} -> {label}" for i, label in enumerate(labels)]
        columns = Columns(labels, padding=1)
        CONSOLE.print(columns)
        CONSOLE.print()

    # If a row label is provided, print the correspondence between the serial number and the label
    if row_labels:
        name, labels = row_labels
        CONSOLE.print(f"Row Labels Denoting [green]{name}[/] Data:")
        labels = [f"Row {i+1} -> {label}" for i, label in enumerate(labels)]
        columns = Columns(labels, padding=1)
        CONSOLE.print(columns)
        CONSOLE.print()


def print_base_data_graph(base_data_list: t.List["BaseData"], *args, **kwargs):
    base_data_list = [base_data for base_data in base_data_list if not base_data.is_raw]
    caption = kwargs.pop("caption", None)
    if caption:
        CONSOLE.print(f"[green]# {caption}", end="\n\n")
    warm_up_data = base_data_list[0]
    if isinstance(warm_up_data.value, list):
        if hasattr(warm_up_data.value[0], "name"):
            print_non_trivial_base_data_graph(base_data_list)
        elif isinstance(warm_up_data.value[0], int):
            if len(warm_up_data.value) != 24 * 7:
                print_non_trivial_base_data_graph(base_data_list)
                return
            data = get_base_data_heatmap_data(base_data_list)
            data = t.cast(t.List[t.List[float]], data)
            print_heatmap(
                data,
                row_labels=(
                    "Week",
                    [
                        "Mon.",
                        "Tue.",
                        "Wed.",
                        "Thu.",
                        "Fri.",
                        "Sat.",
                        "Sun.",
                    ],
                ),
                col_labels=("Time", [f"{i:02}:00" for i in range(24)]),
            )
    else:
        print_trivial_base_data_graph(base_data_list)


def get_trivival_network_heatmap_data(
    netwok_data: "BaseNetworkData",
) -> t.Tuple[
    t.List[t.List[float]],
    t.List[t.Tuple[str, float]],
    t.List[t.Tuple[str, float]],
]:
    node_names = [node.name for node in netwok_data.nodes]
    node_values = [node.value for node in netwok_data.nodes]
    nodes_length = len(node_names)

    heatmap_data = [[0.0] * nodes_length for _ in range(nodes_length)]
    row_labels = col_labels = t.cast(
        t.List[t.Tuple[str, float]], list(zip(node_names, node_values))
    )
    for edge in netwok_data.edges:
        heatmap_data[node_names.index(edge.name0)][
            node_names.index(edge.name1)
        ] = edge.value

    return heatmap_data, row_labels, col_labels


def get_non_trivival_network_heatmap_data(
    netwok_data: "BaseNetworkData",
) -> t.Tuple[
    t.List[t.List[float]],
    t.List[t.Tuple[str, float]],
    t.List[t.Tuple[str, float]],
]:
    node_names = [node["id"] for node in netwok_data.nodes]
    node_values = [node["v"] for node in netwok_data.nodes]
    nodes_length = len(node_names)

    heatmap_data = [[0.0] * nodes_length for _ in range(nodes_length)]
    row_labels = col_labels = t.cast(
        t.List[t.Tuple[str, float]], list(zip(node_names, node_values))
    )
    for edge in netwok_data.edges:
        heatmap_data[node_names.index(edge["s"])][node_names.index(edge["t"])] = edge[
            "w"
        ]

    return heatmap_data, row_labels, col_labels


def print_base_network_data_graph(network_data: "BaseNetworkData", *args, **kwargs):
    caption = kwargs.pop("caption", None)
    if caption:
        CONSOLE.print(f"[green]# {caption}", end="\n\n")

    warm_up_data = network_data.nodes[0]
    if hasattr(warm_up_data, "name"):
        (
            heatmap_data,
            row_labels,
            col_labels,
        ) = get_trivival_network_heatmap_data(network_data)
    else:
        (
            heatmap_data,
            row_labels,
            col_labels,
        ) = get_non_trivival_network_heatmap_data(network_data)

    print_heatmap(
        heatmap_data,
        row_labels=("Source Node Node", row_labels),
        col_labels=("Dest Node Data", col_labels),
    )
