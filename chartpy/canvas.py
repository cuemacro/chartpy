__author__ = 'saeedamen' # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

"""
Canvas

Creates a webpage out of chart objects (and strings)

"""

from chartpy.chart import Chart

class Canvas(object):

    def __init__(self, elements_to_render):
        self.elements_to_render = elements_to_render

    def generate_canvas(self, page_title = 'chartpy dashboard', jupyter_notebook = False, silent_display = True, output_filename = None, canvas_plotter = 'plain', render_pdf=False):

        if canvas_plotter == 'plain':
            canvas_plotter = CanvasPlotterPlain()
        elif canvas_plotter == 'keen':
            canvas_plotter = CanvasPlotterKeen()

        canvas_plotter.render_canvas(self.elements_to_render, page_title=page_title, jupyter_notebook=jupyter_notebook, silent_display=silent_display,
                                     output_filename=output_filename, render_pdf=render_pdf)

#########################################
import abc
import pandas

class CanvasPlotterTemplate(object):

    @abc.abstractmethod
    def render_canvas(self, elements_to_render, jupyter_notebook = False, silent_display = True, output_filename = None, canvas_plotter = None,
                      page_title="chartpy dashboard", render_pdf=False):
        pass

    def output_page(self, html, jupyter_notebook, output_filename, silent_display, render_pdf):
        if output_filename is None:
            import datetime
            html_filename = str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').replace(".", "-") + "-canvas.html"
        else:
            html_filename = output_filename

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.prettify()

        html_file = open(html_filename, "w")
        html_file.write(html)
        html_file.close()

        if (not (silent_display)):
            import webbrowser
            webbrowser.open(html_filename)

        if (jupyter_notebook):
            # from IPython.core.display import display, HTML
            from IPython.display import IFrame, display, HTML

            html = IFrame(html_filename, width=900, height=350, onload="this.style.height=this.contentDocument.body.scrollHeight +'px'")
            # html = HTML('<iframe src="' + html_filename + '" frameborder="0" scrolling="no" width=900 align="middle" '+
            #            """
            #            onload="this.style.height=this.contentDocument.body.scrollHeight +'px';"></iframe>
            #            """)

            # print(html)
            display(html)

        if(render_pdf):
            pdf_filename = html_filename.replace('html', 'pdf')
            pdf_filename = pdf_filename.replace('htm', 'pdf')

            import six

            from xhtml2pdf import pisa

            pdf = six.StringIO()
            resultFile = open(pdf_filename, "w+b")
            from io import StringIO, BytesIO
            pisaStatus = pisa.CreatePDF(StringIO(html), resultFile)

            import ho.xhtml2pdf as xhtml2pdf

            resultFile.close()

            if not pdf.err:
                xhtml2pdf.startViewer(pdf)

class CanvasPlotterPlain(CanvasPlotterTemplate):
    def render_canvas(self, elements_to_render, jupyter_notebook = False, silent_display=True, output_filename=None,
                      page_title="chartpy dashboard", render_pdf=False):

        html = []
        html.append('<head><title>' + page_title + '</title>')
        html.append(plain_css)
        html.append('</head>')

        html.append('<h1>' + page_title + '</h1>')
        html.append('<table cellpadding="0">')

        for i in range(0, len(elements_to_render)):

            row = elements_to_render[i]

            html.append('<tr>\n')

            for j in range(0, len(row)):
                html.append('<td>')

                object = row[j]

                if isinstance(object, Chart):

                    chart = object

                    padding = 40

                    old_margin = chart.style.thin_margin
                    old_silent_display = chart.style.silent_display
                    chart.style.silent_display = True
                    chart.style.thin_margin = True

                    chart.plot()

                    chart.style.thin_margin = old_margin
                    chart.style.silent_display = old_silent_display

                    # grab file name
                    if chart.engine == 'matplotlib':
                        # if (chart.style.file_output is None):
                        #     import time
                        #     chart.style.file_output = str(time.time()) + "matplotlib.png"

                        source_file = chart.style.file_output
                    else:
                        source_file = chart.style.html_file_output

                    try:
                        width = chart.style.width * abs(chart.style.scale_factor) + padding
                        height = chart.style.height * abs(chart.style.scale_factor) + padding

                        #html.append('<div align="center"><div>')
                        html.append('<iframe src="' + source_file + '" width="' + str(width) + \
                               '" height="' + str(height) + '" frameborder="0" scrolling="no"></iframe>')

                        #html.append('</div></div>')
                    except:
                        pass

                    # print(chart.style.html_file_output)
                    # print(chart)
                elif isinstance(object, str):
                    html.append(object)
                elif isinstance(object, pandas.DataFrame):
                    old_width = pandas.get_option('display.max_colwidth')
                    pandas.set_option('display.max_colwidth', -1)

                    html_table = object.to_html(escape=False).replace('border="1"', 'border="0"')
                    html_table = html_table.replace("text-align: right;", "text-align: center; vertical-align: text-top;")

                    html.append(html_table)
                    pandas.set_option('display.max_colwidth', old_width)

                html.append('</td>\n')

            html.append('</tr>\n')

        html.append('</table>\n')

        html = '\n'.join(html)

        self.output_page(html, jupyter_notebook, output_filename, silent_display, render_pdf)

#### based on Keen.io template at https://github.com/plotly/dashboards
class CanvasPlotterKeen(CanvasPlotterTemplate):
    def render_canvas(self, elements_to_render, jupyter_notebook = False, silent_display = True, output_filename = None,
                      page_title='chartpy dashboard', render_pdf=False):

        html = []

        html.append('''
                <!DOCTYPE html>
                <html>
                <head>
                  <title>''')
        html.append(page_title)
        html.append('''</title>
                  <link rel="shortcut icon" href="logo.png" />
                  <link rel="stylesheet" type="text/css" href="static/css/bootstrap.min.css" />
                  <link rel="stylesheet" type="text/css" href="static/css/keen-dashboards.css" />
                  <!-- For slider -->
                  <link rel="stylesheet" type="text/css" href="static/css/iThing.css" />
                </head>
                <body class="application">

                <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
                    <div class="container-fluid">
                      <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                          <span class="sr-only">Toggle navigation</span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                          <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand">
                          <!-- <img src="logo.png" alt="Smiley face" height="23" width="23"> -->
                          <span class="glyphicon glyphicon-chevron-left"></span>
                        </a>
                        <a class="navbar-brand" href="http://www.cuemacro.com">chartpy dashboard </a>
                      </div>
                    </div>
                </div>
                ''')

        html.append('<div class="container-fluid">')

        for i in range(0, len(elements_to_render)):

            row = elements_to_render[i]

            html.append('<div class="row">') # open row

            for j in range(0, len(row)):

                object = row[j]

                if isinstance(object, Chart):

                    chart = object
                    padding = 20

                    html.append('<div style="display:inline-block; width: ' + str(
                        chart.style.width * abs(chart.style.scale_factor) + padding) + 'px">')

                    html.append('<div class="chart-wrapper">')
                    html.append('<div class="chart-title">' + chart.style.title + '</div>')

                    old_scale_factor = chart.style.scale_factor
                    old_silent_display = chart.style.silent_display
                    old_margin = chart.style.thin_margin
                    old_title = chart.style.title
                    old_source = chart.style.source

                    chart.style.silent_display = True
                    chart.style.title = None
                    chart.style.source = None
                    chart.style.thin_margin = True

                    # hack to get bokeh to fit properly in window
                    if chart.engine == 'bokeh':
                        chart.style.scale_factor = 0.9 * chart.style.scale_factor

                    chart.plot()

                    chart.style.silent_display = old_silent_display
                    chart.style.scale_factor = old_scale_factor
                    chart.style.thin_margin = old_margin
                    chart.style.title = old_title
                    chart.style.source = old_source

                    if chart.engine == 'matplotlib':
                        if (chart.style.file_output is None):
                            import time
                            chart.style.file_output = str(time.time()) + "matplotlib.png"

                        source_file = chart.style.file_output
                    else:
                        source_file = chart.style.html_file_output

                    try:
                        html.append('<div style="display:inline-block; height: '
                                    + str(chart.style.height * abs(chart.style.scale_factor) + padding)
                                    + 'px; vertical-align: center" class="chart-stage">')

                        html.append('<iframe src="' + source_file + '" width="' + str(
                            chart.style.width * abs(chart.style.scale_factor) + padding) + \
                               '" height="' + str(chart.style.height * abs(
                            chart.style.scale_factor) + padding) + '" frameborder="0" scrolling="no" align="middle"></iframe>')

                        html.append('</div>')

                        html.append('<div class="chart-notes">' + old_source + '</div>')

                    except:
                        pass

                    html.append('</div>')

                    # print(chart.style.html_file_output)
                    # print(chart)
                elif isinstance(object, str):
                    html.append('<div style="display:inline-block;>')
                    html.append(object)
                    html.append('</div>')
                elif isinstance(object, pandas.DataFrame):
                    html.append('<div style="display:inline-block;>')
                    html.append(object.to_html())
                    html.append('</div>')

                html.append('</div>')

            html.append('</div>')

        html.append('</div>')

        html = '\n'.join(html)

        self.output_page(html, jupyter_notebook, output_filename, silent_display, render_pdf)

plain_css = '''
<style>
a, a:focus, a:hover, a:active {
  color: #00afd7;
}

p, tr {
  font-family: "Open Sans Light", "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

h1, h2, h3 {
  font-family: "Open Sans Light", "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;
  margin: 12px 0;
}
h1 {
  font-size: 32px;
  font-weight: 100;
  letter-spacing: .02em;
  line-height: 48px;
  margin: 12px 0;
}
h2 {
  color: #2a333c;
  font-weight: 200;
  font-size: 21px;
}
h3 {
  color: rgb(84, 102, 120);
  font-size: 21px;
  font-weight: 500;
  letter-spacing: -0.28px;
  line-height: 29.39px;
}

.btn {
  background: transparent;
  border: 1px solid white;
}

.keen-logo {
  height: 38px;
  margin: 0 15px 0 0;
  width: 150px;
}

.navbar-toggle {
  background-color: rgba(255,255,255,.25);
}
.navbar-toggle .icon-bar {
  background: #fff;
}


.navbar-nav {
  margin: 5px 0 0;
}
.navbar-nav > li > a {
  font-size: 15px;
  font-weight: 200;
  letter-spacing: 0.03em;
  padding-top: 19px;
  text-shadow: 0 0 2px rgba(0,0,0,.1);
}
.navbar-nav > li > a:focus,
.navbar-nav > li > a:hover {
  background: transparent none;
}

.navbar-nav > li > a.navbar-btn {
  background-color: rgba(255,255,255,.25);
  border: medium none;
  padding: 10px 15px;
}
.navbar-nav > li > a.navbar-btn:focus,
.navbar-nav > li > a.navbar-btn:hover {
  background-color: rgba(255,255,255,.35);
}
.navbar-collapse {
  box-shadow: none;
}

.masthead {
  background-color: #00afd7;
  background-image: url("../img/bg-bars.png");
  background-position: 0 -290px;
  background-repeat: repeat-x;
  color: #fff;
  margin: 0 0 24px;
  padding: 20px 0;
}
.masthead h1 {
  margin: 0;
}
.masthead small,
.masthead a,
.masthead a:focus,
.masthead a:hover,
.masthead a:active {
  color: #fff;
}
.masthead p {
  color: #b3e7f3;
  font-weight: 100;
  letter-spacing: .05em;
}

.hero {
  background-position: 50% 100%;
  min-height: 450px;
  text-align: center;
}
.hero h1 {
  font-size: 48px;
  margin: 120px 0 0;
}
.hero .lead {
  margin-bottom: 32px;
}
.hero a.hero-btn {
  border: 2px solid #fff;
  display: block;
  font-family: "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 24px;
  font-weight: 200;
  margin: 0 auto 12px;
  padding: 12px 0 6px;
  width: 320px;
}
.hero a.hero-btn:focus,
.hero a.hero-btn:hover {
  border-color: transparent;
  background-color: #fff;
  color: #00afd7;
}

.sample-item {
  margin-bottom: 24px;
}

.signup {
  float: left;
  display: inline-block;
  vertical-align: middle;
  margin-top: -6px;
  margin-right: 10px;
}

.love {
  border-top: 1px solid #d7d7d7;
  color: #546678;
  margin: 24px 0 0;
  padding: 15px 0;
  text-align: center;
}

.love p {
  margin-bottom: 0;
}

td {
    text-align: center;
    vertical-align: text-top;
    font-size: 12px
}

tr {
    text-align: center;
    vertical-align: text-top;
    font-size: 12px
}

</style>
'''