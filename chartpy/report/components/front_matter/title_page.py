from typing import AnyStr, List

import pandas
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer

from chartpy.report.common import ReportBlock


class TitlePage(ReportBlock):
    """Title page of report

    See Also
    --------
    .. ReportBlock
    """

    def __init__(self, report_name: AnyStr) -> None:
        super().__init__(title=report_name, order_priority=-20)

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
            List of reportlab flowables the proceeds the report blocks
            description
        """
        return list()

    def generate_content(self) -> List:
        """Method to generate content based on the input element

        Returns
        -------
        List
            List of reportlab flowables with date the report was generated
        """
        # Generate story
        story = list()

        story.append(Spacer(1, 250))

        metadata = f"""
            <b>Report Generated:</b> 
            {pandas.Timestamp('today'):%Y-%m-%d %H:%M:%S}
        """

        story.append(Paragraph(metadata, self.stylesheet["ReportParagraph"]))

        story.append(NextPageTemplate("portrait"))

        story.append(PageBreak())

        return story
