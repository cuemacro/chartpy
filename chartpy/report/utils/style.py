from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Frame, TableStyle

# Define a stylesheet that can be used
stylesheet = getSampleStyleSheet()

# Register fonts
registerFont(TTFont("Arial", "ARIAL.ttf"))
Font = "Helvetica"

stylesheet.add(
    ParagraphStyle(
        name="ReportTitle",
        fontName=Font,
        fontSize=28,
        leading=64,
        alignment=0,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ReportField",
        fontName=Font,
        fontSize=18,
        leading=30,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ReportSubField",
        fontName=Font,
        fontSize=12,
        leading=22,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ReportParagraph",
        fontName=Font,
        fontSize=9,
        leading=11,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ReportBullet",
        fontName=Font,
        fontSize=9,
        leading=14,
        bulletAnchor=0,
        bulletText="-",
        bulletFontSize=9,
        bulletIndent=10,
        leftIndent=16,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ContentsTitle",
        fontName=Font,
        fontSize=11,
        leading=32,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ContentsField",
        fontName=Font,
        fontSize=11,
        leading=13,
        leftIndent=10,
        spaceBefore=10,
        borderWidth=1,
        borderColor="red",
        borderRadius=1,
        borderPadding=0,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ContentsSubField",
        fontName=Font,
        fontSize=9,
        leading=11,
        leftIndent=20,
        borderWidth=1,
        borderColor="red",
        borderRadius=1,
        borderPadding=0,
    )
)

# Table formatting
stylesheet.add(
    ParagraphStyle(
        name="ReportTableEntries",
        fontName=Font,
        fontSize=5,
        leading=10,
    )
)

stylesheet.add(
    ParagraphStyle(
        name="ReportValueTableEntries",
        fontName=Font,
        fontSize=6,
        leading=10,
    )
)

# Page frames
portrait_title_frame = Frame(
    2.5 * cm,
    2.5 * cm,
    15 * cm,
    25 * cm,
    leftPadding=0,
    rightPadding=0,
    topPadding=0,
    bottomPadding=0,
    id="portrait_title",
)

portrait_frame = Frame(
    2.5 * cm,
    2.5 * cm,
    15 * cm,
    25 * cm,
    leftPadding=0,
    rightPadding=0,
    topPadding=0,
    bottomPadding=0,
    id="portrait",
)

default_table_style = TableStyle(
    [
        ("FONTSIZE", (0, 0), (-1, -1), 5),
        ("TEXTFONT", (0, 0), (-1, -1), Font),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
)
