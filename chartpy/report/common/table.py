import abc
import copy
import tkinter
from tkinter import font as tk_font
from typing import Any, AnyStr, Dict, List

import numpy
import pandas
from reportlab.platypus import Paragraph, Table, TableStyle

from chartpy.report.utils import default_table_style, stylesheet


class TableComponent:
    """A class which handles table objects"""

    # Font attributes
    font_size: int
    font_name: AnyStr
    font: tk_font.Font

    # Table attributes
    style: List[Dict]
    row_height: float

    @abc.abstractmethod
    def generate_table(self, item: Any) -> Table:
        """Abstract method to turn an item into a reportlab table

        Parameters
        ----------
        item : Any
            Input item to turn into table

        Returns
        -------
        Table
            Reportlab table generated from item
        """
        raise NotImplementedError


class DataFrameToTableComponent(TableComponent):
    """A class which handles table objects where the input is a dataframe"""

    index_name: bool
    column_formats: Dict
    column_names: Dict
    row_formats: Dict
    row_names: Dict

    def generate_table(self, df: pandas.DataFrame) -> Table:
        """Generates reportlab table give initial dataframe

        Parameters
        ----------
        df: pandas.DataFrame
            The dataframe to create into a Table object

        Returns
        -------
            Table object
        """
        df_original = copy.deepcopy(df)

        # Format table
        df = df.pipe(self.format_df_columns).pipe(self.remove_nan_values)

        # Calculate dataframe width and height
        df_width = self.measure_width(df)
        df_height = self.measure_height(df)

        # Generate data for the table
        data = self.generate_data(df)

        # Create the reportlab table object
        table = Table(data, df_width, df_height)

        # Style the table
        self.table_style(df_original, table)

        return table

    @property
    def font(self) -> tk_font.Font:
        """Returns the font used in the table

        Returns
        -------
        tk_font.Font
            Font used in reportlab
        """
        tkinter.Frame().destroy()
        return tk_font.Font(
            family=self.font_name, size=self.font_size, weight="bold"
        )

    @staticmethod
    def multi_index_replacer(values: List[AnyStr]) -> List[AnyStr]:
        """Replaces repeated index values with empty strings

        Parameters
        ----------
        values : List[AnyStr]
            Index values

        Returns
        -------
        List[AnyStr]
            Index values with repeated values replaced with empty strings
        """
        return [
            "\n ".join(values[i].split())
            if (i == 0) or values[i] != values[i - 1]
            else ""
            for i in range(len(values))
        ]

    def get_df_columns(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """Helper method to get the dataframe columns into an array

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            Dataframe of columns values
        """
        return pandas.DataFrame(
            [
                self.multi_index_replacer(
                    df.columns.get_level_values(level).astype(str)
                )
                for level in range(df.columns.nlevels)
            ]
        )

    def get_df_index(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """Helper method to get the dataframe index into an array

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            Dataframe of index values
        """
        return pandas.DataFrame(
            [
                self.multi_index_replacer(
                    df.index.get_level_values(level).astype(str)
                )
                for level in range(df.index.nlevels)
            ]
        ).T

    @staticmethod
    def remove_nan_values(df: pandas.DataFrame) -> pandas.DataFrame:
        """Replaces all nan values that were in the original dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            Dataframe with nan values replaced with empty stings
        """
        return df.fillna("")

    def measure_height(self, df: pandas.DataFrame) -> List[float]:
        """Measures the height of the dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        List[float]
            List of the row heights for each row
        """
        row_height = (
            self.get_df_columns(df)
            .map(lambda x: self.row_height * len(x.split()))
            .max(axis=1)
            .values.tolist()
        )
        return row_height + (len(df.index) * [self.row_height])

    def measure_df_width(self, df: pandas.DataFrame) -> List[float]:
        """Measures each individual element of dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        List[float]
            List of the column width for each column
        """
        return (
            df.map(lambda x: self.font.measure(str(x)) + self.font_size)
            .max()
            .values.tolist()
        )

    def measure_width(self, df: pandas.DataFrame) -> List[float]:
        """Measures the width of the dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        List[float]
            List of dataframes width
        """
        # Measure max width of values, columns, and indexes within dataframe
        df_val_width = df.pipe(lambda x: self.measure_df_width(x))
        df_col_width = (
            self.get_df_columns(df)
            # Using 'A' as a standard character size
            .map(
                lambda x: "A"
                * (max([len(w) for w in x.split()]) if x != "" else 0)
            ).pipe(lambda x: self.measure_df_width(x))
        )
        df_index_width = self.get_df_index(df).pipe(
            lambda x: self.measure_df_width(x)
        )

        # Calculating the final column width
        col_width = [
            max(val, col) for val, col in zip(df_val_width, df_col_width)
        ]

        return df_index_width + col_width if self.index_name else col_width

    @staticmethod
    def get_bold_paragraph(df: pandas.DataFrame) -> pandas.DataFrame:
        """Returns mapped dataframe with values replaced with reportlab objects

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            Dataframe with values replaced by reportlab paragraph objects
        """
        return df.map(
            lambda x: Paragraph(
                f"<b>{x}</b>", stylesheet["ReportTableEntries"]
            )
        )

    @staticmethod
    def get_paragraph(df: pandas.DataFrame) -> pandas.DataFrame:
        """Returns mapped dataframe with values replaced with reportlab objects

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            Dataframe with values replaced by reportlab paragraph objects
        """
        return df.map(
            lambda x: Paragraph(f"{x}", stylesheet["ReportValueTableEntries"])
        )

    def generate_data(self, df: pandas.DataFrame) -> object:
        """Method to generate data to populate reportlab table object

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        List
            List of paragraph objects
        """
        df_columns = self.get_df_columns(df).pipe(
            lambda x: self.get_bold_paragraph(x)
        )
        data = numpy.vstack(
            [df_columns, df.pipe(lambda x: self.get_paragraph(x))]
        ).tolist()

        if self.index_name:
            df_index = self.get_df_index(df).pipe(
                lambda x: self.get_bold_paragraph(x)
            )
            filler = numpy.full(
                (len(df_columns), len(df_index.T)), "", dtype=str
            )
            index_data = numpy.vstack([filler, df_index])
            data = numpy.hstack([index_data, data]).tolist()

        return data

    def format_df_columns(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """Method to format the values and rename columns

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        pandas.DataFrame
            DataFrame with columns reformatted
        """
        df_copy = copy.deepcopy(df)
        df_dict = dict()
        # If only one FORMATTER (func) given apply to all columns
        if type(self.column_formats) == set:
            for col in df_copy.columns:
                for func in self.column_formats:
                    df_dict[col] = df[col].apply(func)
        else:
            # This is not great but it provides more freedoms in FORMATTERS
            for col, func in self.column_formats.items():
                df_dict[col] = df[col].apply(func)

        return pandas.concat(df_dict, axis=1).rename(columns=self.column_names)

    def table_style(self, df: pandas.DataFrame, table: Table) -> None:
        """Method to style the table based on values in dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        table : Table
            Reportlab table to be styled
        """
        table.setStyle(default_table_style)
        if self.style is not None:
            for style in self.style:
                table.setStyle(
                    TableStyle(
                        style["func"](df, style["color"], style["mask"])
                    )
                )


class StandardTableComponent(DataFrameToTableComponent):
    """Standard table component"""

    # Font attributes
    font_size: int = 8
    font_name: AnyStr = "Helvetica"

    # Table attributes
    column_formats: Dict = dict()
    column_names: Dict = dict()
    row_formats: Dict = dict()
    row_names: Dict = dict()
    style: List[Dict] = None
    row_height: float = 11
    index_name: bool = True


class NoIndexTableComponent(StandardTableComponent):
    """Standard table component with no index"""

    index_name: bool = False
