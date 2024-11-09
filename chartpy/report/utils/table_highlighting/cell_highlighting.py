from typing import AnyStr, Callable, List

import numpy
import pandas

from chartpy.report.utils.constants import (
    BACKGROUND_BOX,
    BACKGROUND_HIGHLIGHT,
    TABLE_COLOR,
)


def cell_highlight(
    df: pandas.DataFrame, color: AnyStr, mask: Callable
) -> List:
    """Cell highlighting determines which rows and columns from the dataframe
    need highlighting using the mask function. The mask function should
    return the dataframe with values (anything not nan) which should be
    highlighted.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe that will be turned into a reportlab Table
    color : AnyStr
        Colour to highlight row
    mask: Callable
        Function that returns the dataframe with non nan values to highlight

    Return
    ------
    List
        List of TableStyle Tuples
    """

    n_idx_levels = df.index.nlevels - 1
    n_col_levels = df.columns.nlevels - 1

    if mask(df).empty:
        return []

    row, col = numpy.where(mask(df).notna())

    highlight_color = "light" + color

    highlight = [
        BACKGROUND_HIGHLIGHT["cell"](
            row + n_col_levels,
            col + n_idx_levels,
            TABLE_COLOR[highlight_color],
        )
        for row, col in zip(row, col)
    ]

    box = [
        BACKGROUND_BOX["cell"](
            row + n_col_levels, col + n_idx_levels, TABLE_COLOR[color]
        )
        for row, col in zip(row, col)
    ]

    return highlight + box
