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
EngineTemplate

Implemented by EngineBokeh, EnglineMatplotlib and EnginePlotly to do underlying plotting

"""

import abc

from math import log10, floor
import numpy
import pandas

from chartpy.style import Style
from chartpy.chartconstants import ChartConstants

cc = ChartConstants()

class EngineTemplate(object):

    def init(self):
        return

    @abc.abstractmethod
    def plot_chart(self, data_frame, style, type):
        return


    def get_bar_indices(self, data_frame, style, chart_type, bar_ind):
        has_bar = False
        xd = data_frame.index
        no_of_bars = len(data_frame.columns)

        if style.chart_type is not None:
            if isinstance(style.chart_type, list):
                if 'bar' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = style.chart_type.count('bar')
                    has_bar = True
                elif 'stacked' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = 1
                    has_bar = True
            elif 'bar' == style.chart_type:
                xd = bar_ind
                has_bar = True
            elif 'stacked' == style.chart_type:
                xd = bar_ind
                has_bar = True
        else:
            if chart_type == 'bar' or chart_type == 'stacked':
                xd = bar_ind
                has_bar = True

        return xd, bar_ind, has_bar, no_of_bars

    def assign(self, structure, field, default):
        if hasattr(structure, field): default = getattr(structure, field)

        return default

    def assign_list(self, style, field, list):
        if hasattr(style, field):
            list = [str(x) for x in getattr(style, field)]

        return list

    def get_linewidth(self, label, linewidth_1, linewidth_2, linewidth_2_series):
        if label in linewidth_2_series:
            return linewidth_2

        return linewidth_1

    def round_to_1(self, x):
        return round(x, -int(floor(log10(x))))

    def split_data_frame_to_list(self, data_frame, style):
        data_frame_list = []

        if isinstance(data_frame, list):
            data_frame_list = data_frame
        else:
            if style.subplots == True:

                for col in data_frame.columns:
                    data_frame_list.append(
                        pandas.DataFrame(index=data_frame.index, columns=[col], data=data_frame[col]))
            else:
                data_frame_list.append(data_frame)

        return data_frame_list

#######################################################################################################################

from bokeh.plotting import figure, output_file, show, gridplot

class EngineBokeh(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):

        cm = ColorMaster()

        if style.scale_factor > 0:
            scale_factor = style.scale_factor * 2/3
        else:
            scale_factor = style.scale_factor

        try:
            if style.bokeh_plot_mode == "offline_jupyter":
                from bokeh.io import output_notebook
                output_notebook()
        except:
            pass

        try:
            html = style.html_file_output
            if (html is None):
                html = "bokeh.html"

            output_file(html)
        except: pass

        plot_width = int(style.width * scale_factor)
        plot_height = int(style.height * scale_factor)

        data_frame_list = self.split_data_frame_to_list(data_frame, style)

        plot_list = []

        for data_frame in data_frame_list:
            bar_ind = numpy.arange(1, len(data_frame.index) + 1)

            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)

            if type(data_frame.index) == pandas.tslib.Timestamp:
                p1 = figure(
                    x_axis_type = "datetime",
                    plot_width = plot_width,
                    plot_height = plot_height,
                    x_range=(xd[0], xd[-1])
                    )

            # if has a bar than categorical axis
            elif has_bar == True:
                p1 = figure(
                    plot_width = plot_width,
                    plot_height = plot_height,
                    x_range=[str(x) for x in data_frame.index]
                    )

                from math import pi
                p1.xaxis.major_label_orientation = pi/2

            # otherwise numerical axis
            else:
                p1 = figure(
                    plot_width = plot_width,
                    plot_height = plot_height,
                    x_range=(xd[0], xd[-1])
                    )

            # set the fonts
            p1.axis.major_label_text_font_size = str(10) + "pt"
            p1.axis.major_label_text_font = cc.bokeh_font
            p1.axis.major_label_text_font_style = cc.bokeh_font_style

            p1.xaxis.axis_label_text_font_size = str(10) + "pt"
            p1.xaxis.axis_label_text_font = cc.bokeh_font
            p1.xaxis.axis_label_text_font_style = cc.bokeh_font_style
            p1.xaxis.axis_label = style.x_title

            p1.yaxis.axis_label_text_font_size = str(10) + "pt"
            p1.yaxis.axis_label_text_font = cc.bokeh_font
            p1.yaxis.axis_label_text_font_style = cc.bokeh_font_style
            p1.yaxis.axis_label = style.y_title

            p1.legend.location = "top_left"
            p1.legend.label_text_font_size = str(10) + "pt"
            p1.legend.label_text_font = cc.bokeh_font
            p1.legend.label_text_font_style = cc.bokeh_font_style
            p1.legend.background_fill_alpha = 0.75
            p1.legend.border_line_width = 0

            # set chart outline
            p1.outline_line_width = 0

            # Plot.title.text
            p1.title.text_font_size = str(14) + "pt"
            p1.title.text_font = cc.bokeh_font

            # TODO fix label
            # if style.display_source_label:
            #     p1.text([30 * scale_factor, 30 * scale_factor], [0, 0], text = [style.brand_label],
            #         text_font_size = str(10 * scale_factor) + "pt", text_align = "left",
            #         text_font = GraphistyleConstants().bokeh_font)

            color_spec = cm.create_color_list(style, data_frame)
            import matplotlib

            bar_space = 0.2
            bar_width = (1 - bar_space) / (no_of_bars)
            bar_index = 0

            has_bar = False

            # plot each series in the dataframe separately
            for i in range(0, len(data_frame.columns)):
                label = str(data_frame.columns[i])
                glyph_name = 'glpyh' + str(i)

                # set chart type which can differ for each time series
                if isinstance(chart_type, list): chart_type_ord = chart_type[i]
                else: chart_type_ord = chart_type

                # get the color
                if color_spec[i] is None:
                    color_spec[i] = self.get_color_list(i)

                try:
                    color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                except: pass

                yd = data_frame.ix[:,i]

                # plot each time series as appropriate line, scatter etc.
                if chart_type_ord == 'line':
                    linewidth_t = self.get_linewidth(label,
                        style.linewidth, style.linewidth_2, style.linewidth_2_series)

                    if linewidth_t is None: linewidth_t = 1

                    if style.display_legend:
                        p1.line(xd, yd, color = color_spec[i], line_width=linewidth_t, name = glyph_name,
                                legend = label,
                        )
                    else:
                        p1.line(xd, data_frame.ix[:,i], color = color_spec[i], line_width=linewidth_t, name = glyph_name)

                elif(chart_type_ord == 'bar'):
                    bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(1,len(bar_ind) + 1)]
                    bar_pos_right = [x + bar_width for x in bar_pos]

                    if style.display_legend:
                        p1.quad(top=yd, bottom=0 * yd, left=bar_pos, right=bar_pos_right, color=color_spec[i], legend=label)
                    else:
                        p1.quad(top=yd, bottom=0 * yd, left=bar_pos, right=bar_pos_right, color=color_spec[i])

                    bar_index = bar_index + 1
                    bar_ind = bar_ind + bar_width

                elif chart_type_ord == 'scatter':
                    linewidth_t = self.get_linewidth(label,
                        style.linewidth, style.linewidth_2, style.linewidth_2_series)

                    if linewidth_t is None: linewidth_t = 1

                    if style.display_legend:
                        p1.circle(xd, yd, color = color_spec[i], line_width=linewidth_t, name = glyph_name,
                                legend = label,
                        )
                    else:
                        p1.circle(xd, yd, color = color_spec[i], line_width=linewidth_t, name = glyph_name)

                p1.grid.grid_line_alpha = 0.3

            plot_list.append(p1)

        p_final = gridplot(plot_list, ncols=1)

        try:
            p_final.title.text = style.title
        except: pass

        show(p_final)  # open a browser

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette

        return color_palette[i % len(color_palette)]

    def generic_settings(self):
        return

#######################################################################################################################

# matplotlib based libraries
from datetime import timedelta

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.dates import YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator
from matplotlib.ticker import MultipleLocator

class EngineMatplotlib(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):

        self.apply_style_sheet(style)

        # create figure & add a subplot
        fig = plt.figure(figsize = ((style.width * style.scale_factor)/style.dpi,
                                    (style.height * style.scale_factor)/style.dpi), dpi = style.dpi)

        fig.suptitle(style.title, fontsize = 14 * style.scale_factor)

        # matplotlib 1.5
        try:
            cyc = matplotlib.rcParams['axes.prop_cycle']
            color_cycle =  [x['color'] for x in cyc]
        except KeyError:
            # pre 1.5
            pass
            # color_cycle =  matplotlib.rcParams['axes.color_cycle']

        cm = ColorMaster()

        data_frame_list = self.split_data_frame_to_list(data_frame, style)

        subplot_no = 1

        for data_frame in data_frame_list:

            bar_ind = np.arange(0, len(data_frame.index))

            # for bar charts, create a proxy x-axis (then relabel)
            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)

            # plot the lines (using custom palettes as appropriate)
            color_spec = cm.create_color_list(style, data_frame)

            if style.subplots == False and len(data_frame_list) == 1:
                ax = fig.add_subplot(111)
            else:
                ax = fig.add_subplot(2,1,subplot_no)

            subplot_no = subplot_no + 1

            if style.x_title != '': ax.set_xlabel(style.x_title)
            if style.y_title != '': ax.set_ylabel(style.y_title)

            plt.xlabel(style.x_title)
            plt.ylabel(style.y_title)

            # format Y axis
            y_formatter = matplotlib.ticker.ScalarFormatter(useOffset = False)
            ax.yaxis.set_major_formatter(y_formatter)

            # create a second y axis if necessary
            ax2 = []

            if style.y_axis_2_series != []:
                ax2 = ax.twinx()

                # do not use a grid with multiple y axes
                ax.yaxis.grid(False)
                ax2.yaxis.grid(False)

            try:
                # get all the correct colors (and construct gradients if necessary eg. from 'blues')


                # for stacked bar
                yoff_pos = np.zeros(len(data_frame.index.values)) # the bottom values for stacked bar chart
                yoff_neg = np.zeros(len(data_frame.index.values)) # the bottom values for stacked bar chart

                zeros = np.zeros(len(data_frame.index.values))

                # for bar chart
                bar_space = 0.2
                bar_width = (1 - bar_space) / (no_of_bars)
                bar_index = 0

                has_matrix = False

                # some lines we should exclude from the color and use the default palette
                for i in range(0, len(data_frame.columns.values)):

                    if isinstance(chart_type, list): chart_type_ord = chart_type[i]
                    else: chart_type_ord = chart_type

                    if chart_type_ord == 'heatmap':
                        # TODO experimental!
                        # ax.set_frame_on(False)
                        ax.pcolor(data_frame, cmap=plt.cm.Blues, alpha=0.8)
                        # plt.colorbar()
                        has_matrix = True
                        break

                    label = str(data_frame.columns[i])

                    ax_temp = self.get_axis(ax, ax2, label, style.y_axis_2_series)

                    yd = data_frame.ix[:,i]

                    if color_spec[i] is None:
                        color_spec[i] = color_cycle[i % len(color_cycle)]

                    if (chart_type_ord == 'line'):
                        linewidth_t = self.get_linewidth(label,
                                                         style.linewidth, style.linewidth_2, style.linewidth_2_series)

                        if linewidth_t is None: linewidth_t = matplotlib.rcParams['axes.linewidth']

                        ax_temp.plot(xd, yd, label = label, color = color_spec[i],
                                         linewidth = linewidth_t)

                    elif(chart_type_ord == 'bar'):
                        # for multiple bars we need to allocate space properly
                        bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(0,len(bar_ind))]

                        ax_temp.bar(bar_pos, yd, bar_width, label = label, color = color_spec[i])

                        bar_index = bar_index + 1

                    elif(chart_type_ord == 'stacked'):
                        bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(0,len(bar_ind))]

                        yoff = np.where(yd > 0, yoff_pos, yoff_neg)

                        ax_temp.bar(bar_pos, yd, label = label, color = color_spec[i], bottom = yoff)

                        yoff_pos = yoff_pos + np.maximum(yd, zeros)
                        yoff_neg = yoff_neg + np.minimum(yd, zeros)

                        # bar_index = bar_index + 1

                    elif(chart_type_ord == 'scatter'):
                        ax_temp.scatter(xd, yd, label = label, color = color_spec[i])

                        if style.line_of_best_fit is True:
                            self.trendline(ax_temp, xd.values, yd.values, order=1, color= color_spec[i], alpha=1,
                                               scale_factor = style.scale_factor)


                # format X axis
                self.format_x_axis(ax, data_frame, style, has_bar, bar_ind, has_matrix)

            except: pass

            if style.display_source_label == True:
                ax.annotate('Source: ' + style.source, xy = (1, 0), xycoords='axes fraction', fontsize=7 * style.scale_factor,
                            xytext=(-5 * style.scale_factor, 10 * style.scale_factor), textcoords='offset points',
                            ha='right', va='top', color = style.source_color)

            if style.display_brand_label == True:
                self.create_brand_label(ax, anno = style.brand_label, scale_factor = style.scale_factor)

            leg = []
            leg2 = []

            loc = 'best'

            # if we have two y-axis then make sure legends are in opposite corners
            if ax2 != []: loc = 2

            try:
                leg = ax.legend(loc = loc, prop={'size':10 * style.scale_factor})
                leg.get_frame().set_linewidth(0.0)
                leg.get_frame().set_alpha(0)

                if ax2 != []:
                    leg2 = ax2.legend(loc = 1, prop={'size':10 * style.scale_factor})
                    leg2.get_frame().set_linewidth(0.0)
                    leg2.get_frame().set_alpha(0)
            except: pass

            try:
                if style.display_legend is False:
                    if leg != []: leg.remove()
                    if leg2 != []: leg.remove()
            except: pass

        try:
            plt.savefig(style.file_output, transparent=False)
        except: pass


        ####### various matplotlib converters are unstable
        # convert to D3 format with mpld3
        try:
            # output matplotlib charts externally to D3 based libraries
            import mpld3

            if style.display_mpld3 == True:
                mpld3.save_d3_html(fig, style.html_file_output)
                mpld3.show(fig)
        except: pass

        # FRAGILE! convert to Bokeh format
        # better to use direct Bokeh renderer
        try:
            if (style.convert_matplotlib_to_bokeh == True):
                from bokeh.plotting import output_file, show
                from bokeh import mpl

                output_file(style.html_file_output)
                show(mpl.to_bokeh())
        except: pass

        # FRAGILE! convert matplotlib chart to Plotly format
        # recommend using AdapterCufflinks instead to directly plot to Plotly
        try:
            import plotly.plotly as py
            import plotly
            import plotly.tools as tls

            if style.convert_matplotlib_to_plotly == True:
                plotly.tools.set_credentials_file(username = style.plotly_username,
                                                  api_key = style.plotly_api_key)

                py_fig = tls.mpl_to_plotly(fig, strip_style = True)
                plot_url = py.plot_mpl(py_fig, filename = style.plotly_url)
        except:
            pass

        # display in matplotlib window
        try:
            if cc.chartfactory_silent_display == True:
                return fig
            elif style.silent_display == False:
                plt.show()
            else:
                return fig

        except:
            pass

    def apply_style_sheet(self, style):
        # set the matplotlib style sheet & defaults
        matplotlib.rcdefaults()

        # first search ChartPy styles, then try matplotlib
        try: plt.style.use(cc.chartfactory_style_sheet[style.style_sheet])
        except: plt.style.use(style.style_sheet)

        # adjust font size for scale factor
        matplotlib.rcParams.update({'font.size': matplotlib.rcParams['font.size'] * style.scale_factor})

        # do not use offsets/scientific notation
        matplotlib.rcParams.update({'axes.formatter.useoffset': False})

    def format_x_axis(self, ax, data_frame, style, has_bar, bar_ind, has_matrix):

        if has_matrix:
            # ax.colorbar()
            # ax.xticks(rotation=90)
            ax.set_xticks(bar_ind)
            ax.set_xlim([0, len(bar_ind)])
            ax.set_yticks(bar_ind)
            ax.set_ylim([0, len(bar_ind)])
            ax.set_xticklabels(data_frame.columns, minor=False)
            ax.set_yticklabels(data_frame.index, minor=False)

            # ax.plot([], [])

            for y in range(len(data_frame.index)):
                for x in range(len(data_frame.columns)):
                    plt.text(x + 0.5, y + 0.5, '%.0f' % data_frame.loc[y, x],
                         horizontalalignment='center',
                         verticalalignment='center',
                         )

            return

        if has_bar:
            ax.set_xticks(bar_ind)
            ax.set_xticklabels(data_frame.index)
            ax.set_xlim([-1, len(bar_ind)])

            # if lots of labels make text smaller and rotate
            if len(bar_ind) > 6:
                plt.setp(plt.xticks()[1], rotation=90)
                # plt.gca().tight_layout()
                # matplotlib.rcParams.update({'figure.autolayout': True})
                # plt.gcf().subplots_adjust(bottom=5)
                import matplotlib.dates as mdates

                if style.date_formatter is not None:
                    ax.format_xdata = mdates.DateFormatter(style.date_formatter)

                plt.tight_layout()
                # ax.tick_params(axis='x', labelsize=matplotlib.rcParams['font.size'] * 0.5)
            return

        # format X axis
        dates = data_frame.index

        # scaling for time series plots with hours and minutes only (and no dates)
        if hasattr(data_frame.index[0], 'hour') and not(hasattr(data_frame.index[0], 'month')):
            ax.xaxis.set_major_locator(MultipleLocator(86400./3.))
            ax.xaxis.set_minor_locator(MultipleLocator(86400./24.))
            ax.grid(b = True, which='minor', color='w', linewidth=0.5)

        # TODO have more refined way of formating time series x-axis!

        # scaling for time series plots with dates too
        else:
            # to handle dates
            try:
                dates = dates.to_pydatetime()
                diff = data_frame.index[-1] - data_frame.index[0]

                import matplotlib.dates as md

                if style.date_formatter is not None:
                    ax.xaxis.set_major_formatter(md.DateFormatter(style.date_formatter))
                elif diff < timedelta(days = 4):

                    # class MyFormatter(Formatter):
                    #     def __init__(self, dates, fmt='%H:%M'):
                    #         self.dates = dates
                    #         self.fmt = fmt
                    #
                    #     def __call__(self, x, pos=0):
                    #         'Return the label for time x at position pos'
                    #         ind = int(round(x))
                    #         if ind >= len(self.dates) or ind < 0: return ''
                    #
                    #         return self.dates[ind].strftime(self.fmt)
                    #
                    # formatter = MyFormatter(dates)
                    # ax.xaxis.set_major_formatter(formatter)

                    date_formatter = '%H:%M'
                    xfmt = md.DateFormatter(date_formatter)
                    ax.xaxis.set_major_formatter(xfmt)

                    if diff < timedelta(minutes=20):
                        ax.xaxis.set_major_locator(MinuteLocator(byminute=range(60), interval=2))
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=1))
                    elif diff < timedelta(hours=1):
                        ax.xaxis.set_major_locator(MinuteLocator(byminute=range(60), interval=5))
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=2))
                    elif diff < timedelta(hours=6):
                        locator = HourLocator(interval=1)
                        ax.xaxis.set_major_locator(locator)
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=30))
                    elif diff < timedelta(days=3):
                        ax.xaxis.set_major_locator(HourLocator(interval=6))
                        ax.xaxis.set_minor_locator(HourLocator(interval=1))

                elif diff < timedelta(days=10):
                    locator = DayLocator(interval=2)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %y'))

                    day_locator = DayLocator(interval=1)
                    ax.xaxis.set_minor_locator(day_locator)

                elif diff < timedelta(days=40):
                    locator = DayLocator(interval=10)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %y'))

                    day_locator = DayLocator(interval=1)
                    ax.xaxis.set_minor_locator(day_locator)

                elif diff < timedelta(days=365 * 0.5):
                    locator = MonthLocator(bymonthday=1, interval=2)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))

                    months_locator = MonthLocator(interval=1)
                    ax.xaxis.set_minor_locator(months_locator)

                elif diff < timedelta(days=365 * 2):
                    locator = MonthLocator(bymonthday=1, interval=3)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))

                    months_locator = MonthLocator(interval=1)
                    ax.xaxis.set_minor_locator(months_locator)

                elif diff < timedelta(days = 365 * 5):
                    locator = YearLocator()
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))

            except:
                try:
                    # otherwise we have integers, rather than dates
                    # TODO needs smarter more generalised mapping of dates
                    max = dates.max()
                    min = dates.min()

                    big_step = self.round_to_1((max - min)/10)

                    small_step = big_step / 5

                    ax.xaxis.set_major_locator(MultipleLocator(big_step))
                    ax.xaxis.set_minor_locator(MultipleLocator(small_step))

                    plt.xlim(min, max)
                except: pass

    def get_axis(self, ax, ax2, label, y_axis_2_series):

        if label in y_axis_2_series: return ax2

        return ax


    def trendline(self, ax, xd, yd, order=1, color='red', alpha=1, Rval=False, scale_factor = 1):
        """ Make a line of best fit """

        # Calculate trendline
        xd[np.isnan(xd)] = 0
        yd[np.isnan(yd)] = 0

        coeffs = np.polyfit(xd, yd, order)

        intercept = coeffs[-1]
        slope = coeffs[-2]
        if order == 2: power = coeffs[0]
        else: power = 0

        minxd = np.min(xd)
        maxxd = np.max(xd)

        xl = np.array([minxd, maxxd])
        yl = power * xl ** 2 + slope * xl + intercept

        # plot trendline
        ax.plot(xl, yl, color = color, alpha = alpha)

        # calculate R squared
        p = np.poly1d(coeffs)

        ybar = np.sum(yd) / len(yd)
        ssreg = np.sum((p(xd) - ybar) ** 2)
        sstot = np.sum((yd - ybar) ** 2)
        Rsqr = ssreg / sstot

        if Rval == False:
            text = 'R^2 = %0.2f, m = %0.4f, c = %0.4f' %(Rsqr, slope, intercept)

            ax.annotate(text, xy=(1, 1), xycoords='axes fraction', fontsize=8 * scale_factor,
                    xytext=(-5 * scale_factor, 10 * scale_factor), textcoords='offset points',
                    ha='right', va='top')

            # Plot R^2 value
            # ax.text(0.65, 0.95, text, fontsize = 10 * scale_factor,
            #            ha= 'left',
            #            va = 'top', transform = ax.transAxes)
            pass
        else:
            # return the R^2 value:
            return Rsqr

    def create_brand_label(self, ax, anno, scale_factor):
        ax.annotate(anno, xy = (1, 1), xycoords = 'axes fraction',
                    fontsize = 10 * scale_factor, color = 'white',
                    xytext = (0 * scale_factor, 15 * scale_factor), textcoords = 'offset points',
                    va = "center", ha = "center",
                    bbox = dict(boxstyle = "round,pad=0.0", facecolor = cc.chartfactory_brand_color))

#######################################################################################################################
cf = None

try:
    import plotly
    import cufflinks as cf
except: pass

import plotly.plotly

class EnginePlotly(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):

        mode = 'line'

        if style is None: style = Style()

        marker_size = 1

        x = ''; y = ''; z = ''
        fig = None

        scale = 1

        try:
            if (style.plotly_plot_mode == 'offline_html'):
                scale = 2/3
        except:
            pass

        # check other plots implemented by Cufflinks
        if fig is None:

            cm = ColorMaster()

            # create figure
            data_frame_list = self.split_data_frame_to_list(data_frame, style)
            fig_list = []
            cols = []

            for data_frame in data_frame_list:
                cols.append(data_frame.columns)

            cols = list(np.array(cols).flat)

            # get all the correct colors (and construct gradients if necessary eg. from 'Blues')
            # need to change to strings for cufflinks

            color_list = cm.create_color_list(style, [], cols=cols)
            color_spec = []

            # if no colors are specified then just use our default color set from chart constants
            if color_list == [None] * len(color_list):
                color_spec = [None] * len(color_list)

                for i in range(0, len(color_list)):
                    # get the color
                    if color_spec[i] is None:
                        color_spec[i] = self.get_color_list(i)

                    try:
                        color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                    except:
                        pass

            else:
                # otherwise assume all the colors are rgba
                for color in color_list:
                    color = 'rgba' + str(color)
                    color_spec.append(color)

            start = 0

            for i in range(0, len(data_frame_list)):
                data_frame = data_frame_list[i]

                if isinstance(chart_type, list):
                    chart_type_ord = chart_type[i]
                else:
                    chart_type_ord = chart_type

                end = start + len(data_frame.columns)
                color_spec1 = color_spec[start:start + end]
                start = end

                if chart_type_ord == 'surface':
                    fig = data_frame.iplot(kind=chart_type,
                                           title=style.title,
                                           xTitle=style.x_title,
                                           yTitle=style.y_title,
                                           x=x, y=y, z=z,
                                           mode=mode,
                                           size=marker_size,
                                           theme=style.plotly_theme,
                                           bestfit=style.line_of_best_fit,
                                           legend=style.display_legend,
                                           colorscale=style.color,
                                           dimensions=(style.width * style.scale_factor * scale,
                                                       style.height * style.scale_factor * scale),
                                           asFigure=True)

                elif chart_type_ord == 'line':
                    chart_type_ord = 'scatter'
                elif chart_type_ord == 'scatter':
                    mode = 'markers'
                    marker_size = 5
                elif chart_type_ord == 'bubble':
                    x = data_frame.columns[0]
                    y = data_frame.columns[1]
                    z = data_frame.columns[2]

                # special case for choropleth which has yet to be implemented in Cufflinks
                # will likely remove this in the future
                elif chart_type_ord == 'choropleth':

                    for col in data_frame.columns:
                        try:
                            data_frame[col] = data_frame[col].astype(str)
                        except:
                            pass

                    if style.color != []:
                        color = style.color
                    else:
                        color = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
                                 [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

                    text = ''

                    if 'text' in data_frame.columns:
                        text = data_frame['Text']

                    data = [dict(
                        type='choropleth',
                        colorscale=color,
                        autocolorscale=False,
                        locations=data_frame['Code'],
                        z=data_frame[style.plotly_choropleth_field].astype(float),
                        locationmode=style.plotly_location_mode,
                        text=text,
                        marker=dict(
                            line=dict(
                                color='rgb(255,255,255)',
                                width=1
                            )
                        ),
                        colorbar=dict(
                            title=style.units
                        )
                    )]

                    layout = dict(
                        title=style.title,
                        geo=dict(
                            scope=style.plotly_scope,
                            projection=dict(type=style.plotly_projection),
                            showlakes=True,
                            lakecolor='rgb(255, 255, 255)',
                        ),
                    )

                    fig = dict(data=data, layout=layout)

                if chart_type_ord not in ['surface', 'choropleth']:

                    fig = data_frame.iplot(kind=chart_type_ord,
                                           title=style.title,
                                           xTitle=style.x_title,
                                           yTitle=style.y_title,
                                           x=x, y=y, z=z,
                                           subplots=False,
                                           mode=mode,
                                           size=marker_size,
                                           theme=style.plotly_theme,
                                           bestfit=style.line_of_best_fit,
                                           legend=style.display_legend,
                                           color=color_spec1,
                                           dimensions=(style.width * style.scale_factor * scale,
                                                       style.height * style.scale_factor * scale),
                                           asFigure=True)

                fig.update(dict(layout=dict(legend=dict(
                    x=0.05,
                    y=1
                ))))

                fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
                fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))

                fig_list.append(fig)

            if len(fig_list) > 1:
                import cufflinks
                fig = cufflinks.subplots(fig_list)
            else:
                fig = fig_list[0]

        self.publish_plot(fig, style)

    def publish_plot(self, fig, style):
        fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
        fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))

        if style.plotly_plot_mode == 'online':
            plotly.tools.set_credentials_file(username=style.plotly_username, api_key=style.plotly_api_key)

            plotly.plotly.plot(fig, filename=style.plotly_url,
                    world_readable=style.plotly_world_readable,
                    auto_open = not(style.silent_display),
                    asImage=style.plotly_as_image)

        elif style.plotly_plot_mode == 'offline_html':
            if style.html_file_output is not None:
                temp_html = style.html_file_output
            else:
                temp_html = "plotly.html"

            plotly.offline.plot(fig, filename=temp_html, auto_open = not(style.silent_display))

        elif style.plotly_plot_mode == 'offline_jupyter':

            # plot in IPython notebook
            plotly.offline.init_notebook_mode()
            plotly.offline.iplot(fig)

        # plotly.offline.plot(fig, filename=style.file_output, format='png',
        #         width=style.width * style.scale_factor, height=style.height * style.scale_factor)
        try:
            plotly.plotly.image.save_as(fig, filename=style.file_output, format='png',
                                width=style.width * style.scale_factor, height=style.height * style.scale_factor)
        except: pass

    def get_color_list(self, i):
        color_palette = cc.plotly_palette

        return color_palette[i % len(color_palette)]

#######################################################################################################################

class ColorMaster:

    def create_color_list(self, style, data_frame, cols = None):
        if cols is None:
            cols = data_frame.columns

        # get all the correct colors (and construct gradients if necessary eg. from 'blues')
        color = self.construct_color(style, 'color', len(cols) - len(style.color_2_series))
        color_2 = self.construct_color(style, 'color_2', len(style.color_2_series))

        return self.assign_color(cols, color, color_2,
                                 style.exclude_from_color, style.color_2_series)

    def construct_color(self, style, color_field_name, no_of_entries):
        color = []

        if hasattr(style, color_field_name):
            if isinstance(getattr(style, color_field_name), list):
                color = getattr(style, color_field_name, color)
            else:
                try:
                    color = self.create_colormap(no_of_entries, getattr(style, color_field_name))
                except:
                    pass

        return color

    def exclude_from_color(self, style):
        if not (isinstance(style.exclude_from_color, list)):
            style.exclude_from_color = [style.exclude_from_color]

        exclude_from_color = [str(x) for x in style.exclude_from_color]

        return exclude_from_color

    def assign_color(self, labels, color, color_2, exclude_from_color,
                     color_2_series):

        color_list = []

        axis_1_color_index = 0;
        axis_2_color_index = 0

        # convert all the labels to strings
        labels = [str(x) for x in labels]

        # go through each label
        for label in labels:
            color_spec = None

            if label in exclude_from_color:
                color_spec = None

            elif label in color_2_series:
                if color_2 != []:
                    color_spec = self.get_color_code(color_2[axis_2_color_index])
                    axis_2_color_index = axis_2_color_index + 1

            else:
                if color != []:
                    color_spec = self.get_color_code(color[axis_1_color_index])
                    axis_1_color_index = axis_1_color_index + 1

            try:
                color_spec = matplotlib.colors.colorConverter.to_rgba(color_spec)
            except:
                pass

            color_list.append(color_spec)

        return color_list

    def get_color_code(self, code):
        # redefine color names
        dict = cc.chartfactory_color_overwrites

        if code in dict: return dict[code]

        return code

    def create_colormap(self, num_colors, map_name):
        ## matplotlib ref for colors: http://matplotlib.org/examples/color/colormaps_reference.html

        cm = matplotlib.cm.get_cmap(name=map_name)

        return [cm(1. * i / num_colors) for i in range(num_colors)]
