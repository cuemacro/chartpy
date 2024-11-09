import abc
import os
import uuid
from typing import Any, AnyStr

import matplotlib.pyplot as plt
from reportlab.lib import utils
from reportlab.platypus import Image

from chartpy.report.utils.utils import check_folder

from chartpy.report.utils import constants


class ImageComponent:
    """A class which handles caching and generating an image

    Attributes
    ----------
    image : Image
        Image from reportlab
    chart : plt.figure
        Figure object to turn into reportlab image
    width : float
        The width of the image component to be displayed
    height : float
        the height of the image component to be displayed
    temp_directory : AnyStr
        The location of the temporary directory to store the file of the image
    identifier : AnyStr
        Unique identifier for the saved image
    file_name : AnyStr
        The filename of the saved image
    file_location : AnyStr
        The file location of the saved image
    """

    image: Image
    chart: plt.figure
    width: float = None
    height: float

    temp_directory = constants.TEMP_DIRECTORY

    def __init__(self) -> None:
        self.identifier = str(uuid.uuid4())
        self.file_name = self.get_file_name()
        self.file_location = self.file_name + ".png"

    def get_file_name(self) -> AnyStr:
        """Returns file name of image

        Returns
        -------
        AnyStr
            File name for image
        """
        return os.path.join(self.temp_directory, self.identifier)

    def set_size(self) -> None:
        """Sets the size of the image given"""
        img = utils.ImageReader(self.file_location)
        iw, ih = img.getSize()
        aspect = ih / float(iw)

        if self.width is None:
            self.width = iw
        self.height = self.width * aspect

    def write(self) -> None:
        """Saves the image in file location"""
        self.chart.savefig(self.file_name, bbox_inches="tight", dpi=300)

    def create_temp_directory(self) -> None:
        """Checks the temporary directory exists"""
        check_folder(self.temp_directory)

    def generate_image(self, *args: Any, **kwargs: Any) -> Image:
        """Generates an image object for reportlab to consume

        Parameters
        ----------
        args : Any
            Arbitrary arguments for generate chart
        kwargs : Any
            Arbitrary keyword arguments for generate chart

        Returns
        -------
        Image
            Image object for reportlab to consume
        """
        self.create_temp_directory()
        self.chart = self.generate_chart(*args, **kwargs)
        self.write()
        self.set_size()
        return Image(self.file_location, self.width, self.height)

    @abc.abstractmethod
    def generate_chart(self, *args: Any, **kwargs: Any) -> plt.figure:
        """Abstract method to override in child class

        Parameters
        ----------
        args : Any
            Arguments for generation of chart
        kwargs : Any
            Keyword arguments for generation of charts

        Returns
        -------
        plt.figure
            matplotlib figure
        """
        raise NotImplementedError
