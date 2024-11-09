import abc
import os
import uuid
from typing import AnyStr

import dataframe_image
import pandas
from reportlab.lib import utils
from reportlab.platypus import Image

from chartpy.report.utils import constants, check_folder


class StyleTableComponent:
    """A class which handles the transformation of pandas dataframes into style
    tables which are turned into image components for reportlab to digest
    """

    table: Image
    styled_table: pandas.io.formats.style.Styler
    width: float = None
    height: float

    temp_directory = constants.TEMP_DIRECTORY

    def __init__(self) -> None:
        self.identifier = str(uuid.uuid4())
        self.file_name = self.get_file_name()

    def get_file_name(self) -> AnyStr:
        """Method to return filename

        Returns
        -------
        AnyStr
            Filename location
        """
        return os.path.join(self.temp_directory, self.identifier) + ".png"

    # TODO add size calculation of dataframe width so that it is automated
    def get_size(self) -> None:
        """Sets height and width of table"""
        img = utils.ImageReader(self.file_name)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        if self.width is None:
            self.width = iw
        self.height = self.width * aspect

    def write(self) -> None:
        """Saves the style table"""
        dataframe_image.export(self.styled_table, self.file_name)

    def create_temp_directory(self):
        """Creates temporary directory if it doesn't already exist"""
        check_folder(self.temp_directory)

    def generate_styled_table(self, df: pandas.DataFrame) -> Image:
        """Generates the styled table from input dataframe

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe to be turned into a styled table

        Returns
        -------
        Image
            Reportlab image component of styled table
        """
        self.create_temp_directory()
        self.styled_table = self.generate_styler(df)
        self.write()
        self.get_size()
        return Image(self.file_name, self.width, self.height)

    @abc.abstractmethod
    def generate_styler(
        self, df: pandas.DataFrame
    ) -> pandas.io.formats.style.Styler:
        """Method to override and generate the styler

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe to turn into styler object

        Returns
        -------
        pandas.io.formats.style.Styler
            Styled dataframe to display in report
        """
        raise NotImplementedError
