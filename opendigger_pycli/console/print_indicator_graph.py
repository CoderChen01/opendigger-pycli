import math
import typing as t
from functools import partial

from rich.color import blend_rgb
from rich.columns import Columns

from . import CONSOLE

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        BaseNetworkData,
        NameAndValue,
    )

DELIM = ","
POSITIVE_TICK = "▇"
NEGTIVE_TICK = "━"
SM_TICK = "|"
HEATMAP_CHAR = "▓"


def print_header_row():
    CONSOLE.print(
        f"[red]{NEGTIVE_TICK}[/]" + " " + "Negative Value" + "  ", end=""
    )
    CONSOLE.print(
        f"[green]{POSITIVE_TICK}[/]" + " " + "Positive Value" + "  ", end=""
    )
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

    CONSOLE.print(f" {value}" + tail)


def blocks_num_map(
    values: t.List[t.Union[int, float]]
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
        values = [len(data.value) for data in base_data_list]
    else:
        values = [data.value for data in base_data_list]
    neg_blocks_num_map = blocks_num_map(
        [abs(value) for value in values if value < 0]
    )
    positive_blocks_num_map = blocks_num_map(
        [value for value in values if value >= 0]
    )
    for value, data in zip(values, base_data_list):
        label = f"{data.year}-{data.month:02}"
        num_blocks = (
            positive_blocks_num_map(value)
            if value >= 0
            else neg_blocks_num_map(value)
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
    base_data_list: t.List["BaseData[t.List[NameAndValue]]"],
):
    """Print a graph for a list of BaseData objects.
    The graph is a horizontal graph with a label and a bar.
    """
    print_header_row()
    sum_values = [
        sum([nv.value for nv in base_data.value])
        for base_data in base_data_list
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
    CONSOLE.print()


def get_heatmap_data(base_data_list: t.List["BaseData[t.List[int]]"]):
    # Create an array for hours and days
    hours = list(range(24))
    days = ["Sun.", "Sat.", "Fri.", "Thu.", "Wed.", "Tue.", "Mon."]

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

    max_val = max(map(max, data))
    min_val = min(map(min, data))

    # 获取终端的宽度
    console_width = CONSOLE.width

    # 计算行号和列号标签的宽度 (序号从1开始)
    row_label_width = len(str(len(data)))
    col_label_width = len(str(len(data[0])))

    transpose_needed = (col_label_width + 1) * len(
        data[0]
    ) + row_label_width + 3 > console_width

    # 如果需要转置，则交换行和列的标签
    if transpose_needed and row_labels and col_labels:
        row_labels, col_labels = col_labels, row_labels

    # 判断是否需要转置
    if transpose_needed:
        data = list(zip(*data))  # 转置数据
        row_label_width, col_label_width = col_label_width, row_label_width

    # 定义颜色渐变
    def get_color(val):
        linear_ratio = (val - min_val) / (max_val - min_val)
        enhanced_ratio = linear_ratio**0.5
        return blend_rgb((0, 0, 255), (255, 0, 0), enhanced_ratio)

    # 打印数据和字符热力图
    for idx, row in enumerate(data, 1):  # 开始序号为1
        line = f"{idx:{row_label_width}} | "
        for val in row:
            color = get_color(val)
            line += f"[{color.hex}]{HEATMAP_CHAR * (col_label_width + 1)}[/]"
        CONSOLE.print(line)

    # 打印行标签下方的分隔线
    header_spacing = " " * (row_label_width + 2)  # 2 for '| '
    CONSOLE.print(
        header_spacing + "-" * ((col_label_width + 1) * len(data[0]))
    )

    # 打印列标签数字
    col_numbers = "".join(
        [f"{i+1:{col_label_width + 1}}" for i in range(len(data[0]))]
    )  # 从1开始
    CONSOLE.print(header_spacing + col_numbers, end="\n\n")

    # 如果提供了列标签，打印序号与标签的对应关系
    if col_labels:
        name, labels = col_labels
        CONSOLE.print(f"Colunm Labels Denoting [green]{name}[/] Data:")
        labels = [f"Col {i+1} -> {label}" for i, label in enumerate(labels)]
        columns = Columns(labels, padding=1)
        CONSOLE.print(columns)
        CONSOLE.print()

    # 如果提供了行标签，打印序号与标签的对应关系
    if row_labels:
        name, labels = row_labels
        CONSOLE.print(f"Row Labels Denoting [green]{name}[/] Data:")
        labels = [f"Row {i+1} -> {label}" for i, label in enumerate(labels)]
        columns = Columns(labels, padding=1)
        CONSOLE.print(columns)
        CONSOLE.print()


def print_base_data_graph(base_data_list: t.List["BaseData"], *args, **kwargs):
    caption = kwargs.pop("caption", None)
    if caption:
        CONSOLE.print(f"[green]# {caption}", end="\n\n")
    warm_up_data = base_data_list[0]
    if isinstance(warm_up_data.value, list):
        if hasattr(warm_up_data.value[0], "name"):
            print_non_trivial_base_data_graph(base_data_list)
        elif isinstance(warm_up_data.value[0], int):
            if len(warm_up_data.value) != 24 * 7:
                return
            data = get_heatmap_data(base_data_list)
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
    print_trivial_base_data_graph(base_data_list)


def print_base_network_data_graph(
    network_data: "BaseNetworkData", *args, **kwargs
):
    pass
