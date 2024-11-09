import abc
from typing import Any, AnyStr, Dict, List

from chartpy.report.common.report_block import ReportBlock


class ReportComponent(ReportBlock):
    """Report component is an abstraction that facilitates to execution of
    pipelines on the input element

    Attributes
    ----------
    data : Dict[AnyStr, Pipeline]
        Dictionary of data to be displayed within the report

    See Also
    --------
    .. ReportBlock
    """

    def __init__(
        self,
        title: AnyStr,
        data: Dict[AnyStr, Any],
        description: AnyStr = "",
        order_priority: int = 0,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            order_priority=order_priority,
        )
        self.data = data

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
            List of reportlab flowables the proceeds the report blocks
            comments
        """
        raise NotImplementedError
