from typing import Any, AnyStr, List

from chartpy.report.common.report_block import ReportBlock
from chartpy.report.utils import StandardDocTemplate


class Report:
    """A report is a collection of blocks that are concatenated to form a
    longer report

    Attributes
    ----------
    components : List[ReportBlock]
        List of report blocks that could be components or sections
    """

    def __init__(self, components: List[ReportBlock]) -> None:
        self.components = components

    @property
    def ordered_components(self) -> List[ReportBlock]:
        """Returns a sorted list of components by their order priority

        Returns
        -------
        List[ReportBlock]
            Sorted list of report blocks
        """
        return sorted(
            self.components,
            key=lambda x: x.order_priority,
            reverse=False,
        )

    def compile_story(self) -> List:
        """Compile the story for the portfolio

        Returns
        -------
        List
            List of flowables from reportlab
        """
        story = []

        # Extract stories
        for component in self.ordered_components:
            story += component.compile_story()

        return story

    def publish_report(self, fpath: AnyStr) -> None:
        """Publish the report as a PDF file to the specified filepath

        Parameters
        ----------
        fpath : AnyStr
            The path for the output pdf
        """
        compiled_story = self.compile_story()
        template = StandardDocTemplate(filename=fpath)
        template.multiBuild(compiled_story)
