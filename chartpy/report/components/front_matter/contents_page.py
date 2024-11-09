from typing import List

from reportlab.platypus import PageBreak, Paragraph, Spacer
from reportlab.platypus.tableofcontents import TableOfContents

from chartpy.report.common import ReportBlock


class ContentsPage(ReportBlock):
    """Contents page to be placed at the start of reports with multiple
    sections

    See Also
    --------
    .. ReportBlock
    """

    def __init__(self) -> None:
        super().__init__(
            title="Table of Contents",
            order_priority=-19,
        )

    def generate_title(self) -> List:
        """Method to generate a title

        Returns
        -------
        List
            Report block title in reportlab format
        """
        return [
            Paragraph(self.title, self.stylesheet["h1"]),
            Spacer(1, 6),
        ]

    def generate_comment(self) -> List:
        """Method to generate a comment based on the input element

        Returns
        -------
        List
            List of reportlab flowables that proceeds the report blocks
            description
        """
        return list()

    def generate_content(self) -> List:
        """Method to generate content based on the input element

        Returns
        -------
        List
            List of reportlab contents page linked with style sheet objects
        """
        # Generate story
        story = list()

        toc = TableOfContents()

        toc.levelStyles = [
            self.stylesheet["ContentsField"],
            self.stylesheet["ContentsSubField"],
        ]

        story.append(toc)

        story.append(PageBreak())

        return story
