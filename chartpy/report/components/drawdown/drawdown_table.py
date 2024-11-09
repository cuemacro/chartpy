from chartpy.report.common import NoIndexTableComponent
from chartpy.report.utils.constants import FORMATTERS


class DrawdownTablePct(NoIndexTableComponent):
    """Drawdown table with columns formatted and renamed

    See Also
    --------
    .. NoIndexTableComponent
    """

    column_formats = {
        "Peak": FORMATTERS["date"],
        "Valley": FORMATTERS["date"],
        "Recovery": FORMATTERS["date"],
        "Duration": FORMATTERS["int"],
        "Recovery Ratio": FORMATTERS["round"],
        "Max Drawdown": FORMATTERS["pct"],
        "99% Max Drawdown": FORMATTERS["pct"],
    }

    column_names = {
        "Max Drawdown": "Max DD",
        "99% Max Drawdown": "99% Max DD",
    }


class DrawdownTablePL(NoIndexTableComponent):
    """Drawdown table with columns formatted and renamed

    See Also
    --------
    .. NoIndexTableComponent
    """

    column_formats = {
        "Peak": FORMATTERS["date"],
        "Valley": FORMATTERS["date"],
        "Recovery": FORMATTERS["date"],
        "Duration": FORMATTERS["int"],
        "Recovery Ratio": FORMATTERS["round"],
        "Max Drawdown": FORMATTERS["dollar_m"],
        "99% Max Drawdown": FORMATTERS["dollar_m"],
    }

    column_names = {
        "Max Drawdown": "Max DD",
        "99% Max Drawdown": "99% Max DD",
    }
