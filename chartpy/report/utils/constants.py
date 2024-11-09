import pandas
from reportlab.lib import colors

TEMP_DIRECTORY = r"C:\TEMP"

PAGE_WIDTH = 596
PAGE_HEIGHT = 842

COLOUR_MAP = {
    "black": "rgb(0, 0, 0)",
    "grey": "rgb(110, 110, 110)",
    "lightgrey": "rgb(175, 175, 175)",
    "lightblue": "rgb(52, 241, 255)",
    "blue": "rgb(62, 161, 255)",
    "darkblue": "rgb(33, 59, 99)",
}

GRAPH_TEXT_STYLE = {"family": "Helvetica", "size": 9}

GRAPH_TEXT_COLOR = {"color": "#6E6E6E"}

GRAPH_LINE_COLOR = [
    "#CC5500",
    "#FFC000",
    "#3EA1FF",
    "#34F1FF",
    "#AFAFAF",
    "#0b67bf",
]

GRAPH_LINE_STYLE = ["solid", "dashed", "dotted", "dashdot"]

GRAPH_TITLE_FONT = {"fontname": "Helvetica", "size": 22, "color": "#6E6E6E"}


def sign(x):
    return "" if x >= 0 else "-"


FORMATTERS = {
    "dollar_m": lambda x: f"{sign(x)}${abs(x)/1e6:,.2f}m"
    if pandas.notnull(x)
    else x,
    "dollar_k": lambda x: f"{sign(x)}${abs(x)/1e3:,.2f}k"
    if pandas.notnull(x)
    else x,
    "pct": lambda x: f"{x * 1e2:,.2f}%" if pandas.notnull(x) else x,
    "bps": lambda x: f"{x * 1e4:,.1f}" if pandas.notnull(x) else x,
    "round": lambda x: f"{x:,.2f}" if pandas.notnull(x) else x,
    "int": lambda x: int(x) if pandas.notnull(x) else x,
    "str": lambda x: str(x) if pandas.notnull(x) else x,
    "float_2dp": lambda x: f"{x:.2f}" if pandas.notnull(x) else x,
    "date": lambda x: x.strftime("%Y-%m-%d") if pandas.notnull(x) else "",
}

BACKGROUND_HIGHLIGHT = {
    "row": lambda row, color: (
        "BACKGROUND",
        (0, row + 1),
        (-1, row + 1),
        color,
    ),
    "column": lambda column, color: (
        "BACKGROUND",
        (column + 1, 0),
        (column + 1, -1),
        color,
    ),
    "cell": lambda row, column, color: (
        "BACKGROUND",
        (column + 1, row + 1),
        (column + 1, row + 1),
        color,
    ),
}

BACKGROUND_BOX = {
    "row": lambda row, color: (
        "BOX",
        (0, row + 1),
        (-1, row + 1),
        1,
        color,
        None,
        (2, 2, 2),
    ),
    "column": lambda column, color: (
        "BOX",
        (column + 1, 0),
        (column + 1, -1),
        1,
        color,
        None,
        (2, 2, 2),
    ),
    "cell": lambda row, col, color: (
        "BOX",
        (col + 1, row + 1),
        (col + 1, row + 1),
        1,
        color,
        None,
        (2, 2, 2),
    ),
}

TABLE_COLOR = {
    "lightblue": colors.lightblue,
    "lightgreen": colors.palegreen,
    "lightred": colors.pink,
    "lightorange": colors.palegoldenrod,
    "blue": colors.blue,
    "green": colors.green,
    "red": colors.red,
    "orange": colors.orange,
}
