from typing import Any, List, Dict, AnyStr

from reportlab.platypus import PageBreak, Paragraph, Spacer

from chartpy.report.common import ReportComponent
from chartpy.report.components.drawdown.drawdown_table import DrawdownTablePct
from chartpy.report.components.drawdown.drawdowns_chart import DrawdownChart
from chartpy.report.utils import LinkedParagraph


class DrawdownComponent(ReportComponent):
    """Drawdown report block detailing information about drawdowns

    See Also
    --------
    .. ReportComponent
    """

    def __init__(self, title: AnyStr, data: Dict[AnyStr, Any]) -> None:
        super().__init__(
            title=title,
            data=data,
            order_priority=1,
        )

    def generate_comment(self) -> List[Paragraph]:
        """Generated comments

        Return
        ------
        List[Paragraph]
            Comments about drawdowns
        """
        comment = f"""
            This section details the top 5 drawdowns of each asset and gives
            a summary of each drawdown.
            """

        # Parse comments into story
        return [
            Paragraph(comment, self.stylesheet["ReportParagraph"]),
            Spacer(1, 12),
        ]

    def generate_content(self) -> List[Any]:
        """Generate content

        Return
        ------
        List[Any]
            Content about drawdowns showing cumulative performance, underwater
            performance, and a table of the top 5 drawdowns for each stock
        """
        content = list()

        for name, data in self.data.items():
            df_drawdown = (
                data["drawdowns"].sort_values(by="Max Drawdown")
                .reset_index(drop=True)
                .iloc[:5]
            )
            df_cumulative_return = (
                data["timeseries"]["CumulativeReturn"]
                .rename("Cumulative Return")
            )
            df_underwater = (
                data["timeseries"]["UnderwaterReturn"]
                .rename("Underwater")
            )

            content += [
                LinkedParagraph(name, self.stylesheet["ReportSubField"]),
                DrawdownChart().generate_image(
                    cumulative_performance=df_cumulative_return,
                    underwater_performance=df_underwater,
                    drawdown_periods=df_drawdown,
                ),
                Spacer(1, 6),
                DrawdownTablePct().generate_table(df=df_drawdown),
                PageBreak(),
            ]

        # Create the story
        return content
