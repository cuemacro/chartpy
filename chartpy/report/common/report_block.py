import abc
import logging
from typing import AnyStr, List

from reportlab.platypus import Spacer

from chartpy.report.utils import LinkedParagraph, stylesheet


class ReportBlock:
    """ReportBlock is the atomic building block of a report

    Attributes
    ----------
    stylesheet : stylesheet
        The style that the flowables use
    logger : logging.Logger
        The logger used within the report block to record information
    name : AnyStr
        The name of the report block
    title : AnyStr
        The title of the block (block begins with title)
    description : AnyStr
        A description of the report block
    order_priority : int
        The priority in block ordering in report (lower values more important)
    """

    stylesheet = stylesheet

    def __init__(
        self,
        title: AnyStr,
        description: AnyStr = "",
        order_priority: int = 0,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = self.__class__.__name__
        self.title = title
        self.description = description
        self.order_priority = order_priority

    def generate_title(self) -> List:
        """Method to generate a title

        Returns
        -------
        List
            Report block title in reportlab format
        """
        return [
            LinkedParagraph(self.title, self.stylesheet["ReportField"]),
            Spacer(1, 3),
        ]

    def generate_description(self) -> List:
        """Method to generate a description

        Returns
        -------
        List
            Report block description in reportlab format
        """
        return [
            LinkedParagraph(
                self.description, self.stylesheet["ReportParagraph"]
            ),
            Spacer(1, 3),
        ]

    @abc.abstractmethod
    def generate_comment(self) -> List:
        """Method to generate a comment based on the input element

        Returns
        -------
        List
            List of reportlab flowables the proceeds the report blocks
            description
        """
        raise NotImplementedError

    @abc.abstractmethod
    def generate_content(self) -> List:
        """Method to generate content based on the input element

        Returns
        -------
        List
            List of reportlab flowables that proceeds the report blocks
            comments
        """
        raise NotImplementedError

    def compile_story(self) -> List:
        """Method to compile the story.

        Returns
        -------
        List
            Compiled Story
        """
        return (
            self.generate_title()
            + self.generate_description()
            + self.generate_comment()
            + self.generate_content()
        )
