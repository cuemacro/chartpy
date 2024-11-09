from typing import AnyStr, Callable, List

import numpy
import pandas

from chartpy.report.utils.constants import (
    BACKGROUND_BOX,
    BACKGROUND_HIGHLIGHT,
    TABLE_COLOR,
)


def row_highlight(
    df: pandas.DataFrame, color: AnyStr, rows_mask: Callable
) -> List:
    """Row highlighting determines which rows from the dataframe need
    highlighting using the row_mask function. The row_mask function should
    return the dataframe index which should be highlighted.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe that will be turned into a reportlab Table
    color: AnyStr
        Colour to highlight row
    rows_mask: Callable
        Function that returns the index of the dataframe to highlight

    Return
    ------
    List
        List of TableStyle Tuples
    """

    n_column_levels = df.columns.nlevels - 1

    if rows_mask(df).empty:
        return []

    row_idx = numpy.where([df.index == row for row in rows_mask(df)])[1]

    highlight_color = "light" + color

    highlight = [
        BACKGROUND_HIGHLIGHT["row"](
            row + n_column_levels, TABLE_COLOR[highlight_color]
        )
        for row in row_idx
    ]

    box = [
        BACKGROUND_BOX["row"](row + n_column_levels, TABLE_COLOR[color])
        for row in row_idx
    ]

    return highlight + box


def top_absolute_rows_mask(df, column, nrows):
    """Helper method to create a mask for top rows for row highlighting"""
    return df[column].abs().sort_values(ascending=False).head(nrows).index


def top_rows_mask(df, column, nrows):
    """Helper method to create a mask for top rows for row highlighting"""
    return df[column].sort_values(ascending=False).head(nrows).index


def bottom_rows_mask(df, column, nrows):
    """Helper method to create a mask for bottom rows for row highlighting"""
    return df[column].sort_values(ascending=True).head(nrows).index


def filter_rows_mask(
    df, column, lower_bound=-numpy.inf, upper_bound=numpy.inf
):
    """Helper method to create a mask based on a filter for row highlighting"""
    return (
        df.loc[lambda x: x[column] > lower_bound]
        .loc[lambda x: x[column] < upper_bound]
        .index
    )
