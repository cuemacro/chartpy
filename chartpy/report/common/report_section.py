from typing import AnyStr, List

from reportlab.platypus import PageBreak, Spacer

from chartpy.report.common.report_block import ReportBlock
from chartpy.report.common.report_component import ReportComponent


class ReportSection(ReportBlock):
    """Report section is a collection of report components

    Attributes
    ----------
    components : List[ReportComponent]
        List of report components to group together

    See Also
    --------
    .. ReportBlock
    """

    def __init__(
        self,
        title: AnyStr,
        components: List[ReportComponent],
        description: AnyStr = "",
        order_priority: int = 0,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            order_priority=order_priority,
        )
        self.components = components

    @property
    def sorted_components(self) -> List[ReportBlock]:
        """Sorted components

        Returns
        -------
        List[ReportBlock]
            List of sorted report blocks based on order priority
        """
        return sorted(
            self.components,
            key=lambda x: x.order_priority,
            reverse=False,
        )

    def generate_comment(self) -> List:
        """Method to generate a comment based on the section

        Returns
        -------
        List
            List of reportlab flowables the proceeds the report blocks
            description
        """
        return list()

    def generate_content(self) -> List:
        """Generate all content from all components

        Returns
        -------
        List of all components titles, descriptions, comments, and contents
        in order of priority with space in between

        """
        return [
            component.compile_story() + [Spacer(1, 18)]
            for component in self.sorted_components
        ]

    def compile_story(self) -> List:
        """Compiles the story with option of ignoring all comments

        Returns
        -------
        List
            Compiled story
        """
        return super().compile_story() + [PageBreak()]
