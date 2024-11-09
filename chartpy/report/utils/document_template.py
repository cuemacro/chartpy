from hashlib import sha1
from typing import Any, AnyStr

from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph

from chartpy.report.utils.style import portrait_frame, portrait_title_frame


class StandardDocTemplate(BaseDocTemplate):
    """Standard template used for pdf generation

    Parameters
    ----------
    filename : AnyStr
        Filename to save pdf
    kwargs : Any
    """

    def __init__(self, filename: AnyStr, **kwargs: Any) -> None:
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename=filename, **kwargs)
        templates = self.get_templates()
        self.addPageTemplates(templates)

    def afterFlowable(self, flowable) -> None:
        """Method to perform after flowable, specifically link paragraphs
        and linked paragraphs to the contents page

        Parameters
        ----------
        flowable : Flowable
            Flowable object that is an element in a story
        """
        if flowable.__class__.__name__ in ["Paragraph", "LinkedParagraph"]:
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == "ReportField":
                level = 0
            elif style == "ReportSubField":
                level = 1
            else:
                return

            E = [level, text, self.page]

            bn = getattr(flowable, "_bookmarkName", None)
            if bn is not None:
                E.append(bn)
            self.notify("TOCEntry", tuple(E))

    @staticmethod
    def make_portrait_title(canvas, doc) -> None:
        """Method to make portrait title page"""
        canvas.saveState()
        canvas.setPageSize(A4)
        canvas.restoreState()

    @staticmethod
    def make_portrait(canvas, doc) -> None:
        """Method to make portrait default page"""
        canvas.saveState()
        canvas.setPageSize(A4)
        canvas.setFont("Arial", 7)
        page = "%s" % (canvas._pageNumber)
        canvas.drawString(A4[0] - 40, A4[1] - 40, page)
        canvas.restoreState()

    def get_templates(self):
        """Method to return list of page templates"""
        portrait_title_template = PageTemplate(
            id="portrait_title",
            frames=[portrait_title_frame],
            onPage=self.make_portrait_title,
        )

        portrait_template = PageTemplate(
            id="portrait", frames=[portrait_frame], onPage=self.make_portrait
        )

        templates = [portrait_title_template, portrait_template]
        return templates


class LinkedParagraph(Paragraph):
    """Linked paragraph with hyperlinks on the title page"""

    def __init__(self, text, style):
        bn = sha1((text + style.name).encode("utf-8")).hexdigest()
        super().__init__(text + '<a name="%s"/>' % bn, style)
        self._bookmarkName = bn
