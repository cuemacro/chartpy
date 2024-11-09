import matplotlib
import matplotlib.pyplot as plt
import pandas
from reportlab.lib.units import cm

from chartpy.report.common import ImageComponent
from chartpy.report.utils import constants


class DrawdownChart(ImageComponent):
    """Drawdown chart showing cumulative performance and underwater performance
    with the drawdowns highlighted

    See Also
    --------
    .. ImageComponent
    """

    width = 15 * cm

    def __init__(self, field_formatter=constants.FORMATTERS["pct"]):
        super().__init__()
        self.field_formatter = field_formatter

    def generate_chart(
        self,
        cumulative_performance: pandas.Series,
        underwater_performance: pandas.Series,
        drawdown_periods: pandas.DataFrame,
    ) -> plt.figure:
        """Generates chart

        Parameters
        ----------
        cumulative_performance : pandas.DataFrame
            Cumulative performance of returns
        underwater_performance : pandas.DataFrame
            Underwater performance of cumulative returns
        drawdown_periods : pandas.DataFrame
            Dataframe of top drawdowns to be marked on the cumulative graph

        Returns
        -------
        plt.figure
            Matplotlib plot with 2 subplots of cumulative returns and
            underwater returns with the top drawdowns marked
        """
        matplotlib.rc("xtick", **constants.GRAPH_TEXT_COLOR)
        matplotlib.rc("ytick", **constants.GRAPH_TEXT_COLOR)

        fig, (ax1, ax2) = plt.subplots(
            nrows=2,
            ncols=1,
            sharex="all",
            gridspec_kw={"height_ratios": [3, 1]},
            figsize=(10, 6),
        )

        # Add cumulative returns with highlight periods of drawdowns
        ax1.plot(
            cumulative_performance,
            color=constants.GRAPH_LINE_COLOR[-1],
            linestyle=constants.GRAPH_LINE_STYLE[0],
        )

        ax1.set_title("Top 5 Drawdown Periods")
        ax1.set_ylabel(cumulative_performance.name, rotation=90)
        ax1.tick_params(axis="x", width=0.2)
        ax1.tick_params(axis="y", length=0.2)
        ax1.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(
                lambda x, p: self.field_formatter(x)
            )
        )

        ax1.grid(
            axis="both",
            alpha=1.0,
            color="black",
            linestyle="dashed",
            linewidth=0.2,
        )

        y_min, y_max = ax1.get_ylim()

        for peak, recovery in drawdown_periods[["Peak", "Recovery"]].values:
            if pandas.isna(recovery):
                # Still underwater, fill to the end of time-series
                recovery = cumulative_performance.index[-1]

            ax1.fill_between(
                [pandas.Timestamp(peak), pandas.Timestamp(recovery)],
                y_min,
                y_max,
                alpha=0.1,
                color="r"
            )

        ax1.axhline(y=0, color="k", linestyle="--")

        # Add underwater chart
        ax2.plot(
            underwater_performance,
            color=constants.GRAPH_LINE_COLOR[-1],
            linestyle=constants.GRAPH_LINE_STYLE[0],
        )

        ax2.set_xlabel("Date")
        ax2.set_ylabel(underwater_performance.name, rotation=90)
        ax2.tick_params(axis="x", width=0.2)
        ax2.tick_params(axis="y", length=0.2)
        ax2.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(
                lambda x, p: self.field_formatter(x)
            )
        )

        ax2.grid(
            axis="both",
            alpha=1.0,
            color="black",
            linestyle="dashed",
            linewidth=0.2,
        )

        ax2.fill_between(
            underwater_performance.index,
            underwater_performance.values,
            where=underwater_performance.values <= 0,
            color=constants.GRAPH_LINE_COLOR[2],
            alpha=0.2,
            label="Drawdown",
        )

        ax2.axhline(y=0, color="k", linestyle="--")
        ax2.axhline(
            y=underwater_performance.mean(),
            color="r",
            linestyle="--",
            label="Average",
        )
        ax1.set_xlim(
            underwater_performance.index[0], underwater_performance.index[-1]
        )
        ax2.set_xlim(
            underwater_performance.index[0], underwater_performance.index[-1]
        )
        ax2.legend(loc="lower left")

        return fig
