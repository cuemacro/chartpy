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
import datetime
from chartpy.style import Style
from chartpy.chartconstants import ChartConstants

cc = ChartConstants()

class EngineTemplate(object):

    def init(self):
        return

    @abc.abstractmethod
    def plot_chart(self, data_frame, style, type):
        return

    def get_time_stamp(self):
        return str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').replace(".", "-")

    def get_bar_indices(self, data_frame, style, chart_type, bar_ind):
        has_bar = 'no-bar'
        xd = data_frame.index
        no_of_bars = len(data_frame.columns)

        if style.chart_type is not None:
            if isinstance(style.chart_type, list):
                if 'bar' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = style.chart_type.count('bar')
                    has_bar = 'barv'
                elif 'stacked' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = 1
                    has_bar = 'barv'
            elif 'bar' == style.chart_type:
                xd = bar_ind
                has_bar = 'barv'
            elif 'barh' == style.chart_type:
                xd = bar_ind
                has_bar = 'barh'
            elif 'stacked' == style.chart_type:
                xd = bar_ind
                has_bar = 'barh'
        else:
            if chart_type == 'bar' or chart_type == 'stacked':
                xd = bar_ind
                has_bar = 'barv'

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

    def generate_file_names(self, style, engine):
        if style.html_file_output is not None and not (style.auto_generate_html_filename):
            pass
        else:
            import time
            style.html_file_output = (self.get_time_stamp() + "-" + engine + ".html")
            style.auto_generate_html_filename = True

        if style.file_output is not None and not (style.auto_generate_filename):
            pass
        else:
            import time
            style.file_output = (self.get_time_stamp() + "-" + engine + ".png")
            style.auto_generate_filename = True

        return style

    def get_max_min_dataframes(self, data_frame_list):
        """Gets minimum and maximum values for a series of dataframes. Can be particularly useful for adjusting colormaps
        for lightness/darkness.

        Parameters
        ----------
        data_frame_list : DataFrame (list)
            DataFrames to be checked

        Returns
        -------
        float, float
            Minimum and maximum values
        """

        import sys

        minz = sys.float_info.max
        maxz = sys.float_info.min

        for data_frame in data_frame_list:

            minz_1 = data_frame.min(axis=0).min()
            maxz_1 = data_frame.max(axis=0).max()

            if minz_1 != numpy.nan:
                minz = min(minz, minz_1)

            if maxz_1 != numpy.nan:
                maxz = max(maxz, maxz_1)


        return minz, maxz

#######################################################################################################################

from bokeh.plotting import figure, output_file, show, gridplot, save
from bokeh.models import Range1d
from bokeh.charts import HeatMap

class EngineBokeh(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):

        cm = ColorMaster()

        if style.scale_factor > 0:
            scale_factor = abs(style.scale_factor) * 2/3
        else:
            scale_factor = abs(style.scale_factor)

        try:
            if style.bokeh_plot_mode == "offline_jupyter":
                from bokeh.io import output_notebook
                output_notebook()
        except:
            pass

        try:
            style = self.generate_file_names(style, 'bokeh')

            output_file(style.html_file_output)
        except: pass

        data_frame_list = self.split_data_frame_to_list(data_frame, style)

        plot_list = []

        plot_width = int((style.width * scale_factor))
        plot_height = int((style.height * scale_factor) / len(data_frame_list))

        for data_frame in data_frame_list:
            bar_ind = numpy.arange(1, len(data_frame.index) + 1)

            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)

            separate_chart = False

            if chart_type == 'heatmap':
                # TODO

                p1 = HeatMap(data_frame,
                             title='Random', plot_width = plot_width, plot_height = plot_height)

                separate_chart = True

            # if has a vertical bar than categorical x-axis
            elif has_bar == 'barv':
                p1 = figure(
                    plot_width = plot_width,
                    plot_height = plot_height,
                    x_range=[str(x).replace(':','.') for x in data_frame.index]
                    )

                from math import pi
                p1.xaxis.major_label_orientation = pi/2
            elif type(data_frame.index) == pandas.tslib.Timestamp or (type(xd[0]) == pandas.tslib.Timestamp and type(xd[-1]) == pandas.tslib.Timestamp):
                p1 = figure(
                    x_axis_type = "datetime",
                    plot_width = plot_width,
                    plot_height = plot_height,
                    # x_range=(xd[0], xd[-1])   # at present Bokeh doesn't like to set limits with datetime, hopefully will change!
                )

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
            p1.xaxis.visible = style.x_axis_showgrid

            p1.yaxis.axis_label_text_font_size = str(10) + "pt"
            p1.yaxis.axis_label_text_font = cc.bokeh_font
            p1.yaxis.axis_label_text_font_style = cc.bokeh_font_style
            p1.yaxis.axis_label = style.y_title
            p1.yaxis.visible = style.y_axis_showgrid

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

            has_bar ='no-bar'

            if not(separate_chart):

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
                    elif (chart_type_ord == 'barh'):
                        # TODO
                        pass

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

                # p1.min_border_left = -40
                # p1.min_border_right = 0
                # p1.min_border_top = 0
                # p1.min_border_bottom = 0

                p1.min_border = -50

            plot_list.append(p1)

        p_final = gridplot(plot_list, ncols=1)

        try:
            p_final.title.text = style.title
        except: pass

        if style.silent_display:
            save(p_final)
        else:
            show(p_final)  # open a browser

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette

        return color_palette[i % len(color_palette)]

    def generic_settings(self):
        return

######################################################################################################################

try:
    from IPython.display import display
    from bqplot import (
        OrdinalScale, LinearScale, Bars, Lines, Axis, Figure
    )
except:
    pass

class EngineBqplot(EngineTemplate):
    def plot_chart(self, data_frame, style, chart_type):
        pass
        # TODO

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette

        return color_palette[i % len(color_palette)]

    def generic_settings(self):
        return

#######################################################################################################################

# vispy based plots

try:
    from vispy import plot as vp
except:
    pass

class EngineVisPy(EngineTemplate):
    def plot_chart(self, data_frame, style, chart_type):

        cm = ColorMaster()

        scale_factor = abs(style.scale_factor)

        try:
            if style.vispy_plot_mode == "offline_jupyter":
                pass
        except:
            pass

        try:
            style = self.generate_file_names(style, 'vispy')
        except:
            pass

        data_frame_list = self.split_data_frame_to_list(data_frame, style)

        plot_list = []

        plot_width = int((style.width * scale_factor))
        plot_height = int((style.height * scale_factor) / len(data_frame_list))

        fig = vp.Fig(size=(plot_width, plot_height), show=False, title=style.title)

        for data_frame in data_frame_list:
            bar_ind = numpy.arange(1, len(data_frame.index) + 1)

            if data_frame.index.name == 'Date':
                data_frame = data_frame.copy()
                data_frame = data_frame.reset_index()
                data_frame = data_frame.drop(['Date'], axis=1)

            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)

            # make the x-axis float as a temporary fix, vispy can't handle Date labels
            separate_chart = False

            # axis properties
            color_spec = cm.create_color_list(style, data_frame)

            import matplotlib

            bar_space = 0.2
            bar_width = (1 - bar_space) / (no_of_bars)
            bar_index = 0

            separate_chart = False

            if chart_type == 'surface':
                # TODO


                separate_chart = True

            has_bar = 'no-bar'

            if not (separate_chart):

                # plot each series in the dataframe separately
                for i in range(0, len(data_frame.columns)):
                    label = str(data_frame.columns[i])
                    glyph_name = 'glpyh' + str(i)

                    # set chart type which can differ for each time series
                    if isinstance(chart_type, list):
                        chart_type_ord = chart_type[i]
                    else:
                        chart_type_ord = chart_type

                    # get the color
                    if color_spec[i] is None:
                        color_spec[i] = self.get_color_list(i)

                    try:
                        color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                    except:
                        pass

                    yd = data_frame.ix[:, i]

                    # plot each time series as appropriate line, scatter etc.
                    if chart_type_ord == 'line':
                        fig[0, 0].plot(np.array((xd, yd)).T, marker_size=0, color=color_spec[i])

                        # TODO
                        pass

                    elif (chart_type_ord == 'bar'):
                        # TODO
                        pass
                    elif (chart_type_ord == 'barh'):
                        # TODO
                        pass

                    elif chart_type_ord == 'scatter':
                        # TODO
                        pass


        if style.silent_display:
            pass
        else:
            if style.save_fig:
                import vispy.io as io
                io.write_png(style.file_output, fig.render())

            fig.show(run=True)


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
from mpl_toolkits.mplot3d import axes3d
import numpy as np

from matplotlib.dates import YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator
from matplotlib.ticker import MultipleLocator

class EngineMatplotlib(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):

        self.apply_style_sheet(style)

        if style.xkcd:
            plt.xkcd()

        # create figure & add a subplot
        fig = plt.figure(figsize = ((style.width * abs(style.scale_factor))/style.dpi,
                                    (style.height * abs(style.scale_factor))/style.dpi), dpi = style.dpi)

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

        first_ax = None

        movie_frame = []

        ordinal = 0

        minz, maxz = self.get_max_min_dataframes(data_frame_list=data_frame_list)

        for data_frame in data_frame_list:
            bar_ind = np.arange(0, len(data_frame.index))

            # for bar charts, create a proxy x-axis (then relabel)
            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)

            ax, ax2, subplot_no, ordinal = self._create_subplot(fig, chart_type, style, subplot_no, first_ax, ordinal)

            # for stacked bar
            yoff_pos = np.zeros(len(data_frame.index.values))  # the bottom values for stacked bar chart
            yoff_neg = np.zeros(len(data_frame.index.values))  # the bottom values for stacked bar chart

            zeros = np.zeros(len(data_frame.index.values))

            # for bar chart
            bar_space = 0.2
            bar_width = (1 - bar_space) / (no_of_bars)
            bar_index = 0

            try:
                has_matrix = 'no'

                if not(isinstance(chart_type, list)):

                    ax_temp = ax

                    # get all the correct colors (and construct gradients if necessary eg. from 'blues')
                    color = style.color

                    if style.color == []:
                        color = cc.chartfactory_default_colormap
                    else:
                        if isinstance(style.color, list):
                            color = style.color[subplot_no - 1]

                    if chart_type == 'heatmap':
                        ax_temp.set_frame_on(False)

                        # weird hack, otherwise comes out all inverted!
                        data_frame = data_frame.iloc[::-1]

                        if style.normalize_colormap:
                            movie_frame.append(ax_temp.pcolor(data_frame.values, cmap=color, alpha=0.8, vmax=maxz, vmin=minz))
                        else:
                            movie_frame.append(ax_temp.pcolor(data_frame.values, cmap=color, alpha=0.8))

                        has_matrix = '2d-matrix'
                    elif chart_type == 'surface':

                        # TODO still very early alpha
                        X, Y = np.meshgrid(range(0, len(data_frame.columns)), range(0, len(data_frame.index)))
                        Z = data_frame.values

                        if style.normalize_colormap:
                            movie_frame.append(ax_temp.plot_surface(X, Y, Z, cmap=color, rstride=1, cstride=1,
                                                                    vmax=maxz, vmin=minz))
                        else:
                            movie_frame.append(ax_temp.plot_surface(X, Y, Z, cmap=color, rstride=1, cstride=1))

                        has_matrix = '3d-matrix'

                if (has_matrix == 'no'):
                    # plot the lines (using custom palettes as appropriate)
                    color_spec = cm.create_color_list(style, data_frame)

                    # some lines we should exclude from the color and use the default palette
                    for i in range(0, len(data_frame.columns.values)):

                        if isinstance(chart_type, list): chart_type_ord = chart_type[i]
                        else: chart_type_ord = chart_type

                        label = str(data_frame.columns[i])

                        ax_temp = self.get_axis(ax, ax2, label, style.y_axis_2_series)

                        yd = data_frame.ix[:,i]

                        if color_spec[i] is None:
                            color_spec[i] = color_cycle[i % len(color_cycle)]

                        if (chart_type_ord == 'line'):
                            linewidth_t = self.get_linewidth(label,
                                                             style.linewidth, style.linewidth_2, style.linewidth_2_series)

                            if linewidth_t is None: linewidth_t = matplotlib.rcParams['axes.linewidth']

                            movie_frame.append(ax_temp.plot(xd, yd, label = label, color = color_spec[i],
                                         linewidth = linewidth_t),)

                        elif(chart_type_ord == 'bar'):
                            # for multiple bars we need to allocate space properly
                            bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(0,len(bar_ind))]

                            movie_frame.append(ax_temp.bar(bar_pos, yd, bar_width, label = label, color = color_spec[i]))

                            bar_index = bar_index + 1

                        elif (chart_type_ord == 'barh'):
                            # for multiple bars we need to allocate space properly
                            bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(0, len(bar_ind))]

                            movie_frame.append(ax_temp.barh(bar_pos, yd, bar_width, label=label, color=color_spec[i]))

                            bar_index = bar_index + 1

                        elif(chart_type_ord == 'stacked'):
                            bar_pos = [k - (1 - bar_space) / 2. + bar_index * bar_width for k in range(0,len(bar_ind))]

                            yoff = np.where(yd > 0, yoff_pos, yoff_neg)

                            movie_frame.append(ax_temp.bar(bar_pos, yd, label = label, color = color_spec[i], bottom = yoff))

                            yoff_pos = yoff_pos + np.maximum(yd, zeros)
                            yoff_neg = yoff_neg + np.minimum(yd, zeros)

                            # bar_index = bar_index + 1

                        elif(chart_type_ord == 'scatter'):
                            movie_frame.append(ax_temp.scatter(xd, yd, label = label, color = color_spec[i]))

                            if style.line_of_best_fit is True:
                                self.trendline(ax_temp, xd.values, yd.values, order=1, color= color_spec[i], alpha=1,
                                               scale_factor = abs(style.scale_factor))

                # format X axis
                self.format_x_axis(ax_temp, data_frame, style, has_bar, bar_ind, bar_width, has_matrix)

            except Exception as e:
                pass
                # print(str(e))

            self._create_legend(ax, ax2, style)

        try:
            ax_temp.set_zlim(minz, maxz)
        except:
            pass

        anim = None

        # should we animate the figure?
        if style.animate_figure:

            if style.animate_titles is None:
                titles = range(1, len(data_frame_list) + 1)
            else:
                titles = style.animate_titles

            # initialization function: weirdly need to plot the last one (otherwise get ghosting!)
            def init():
                return [movie_frame[-1]]

            def update(i):
                fig.canvas.set_window_title(str(titles[i]))

                return [movie_frame[i]]

            import matplotlib.animation as animation

            try:
                anim = animation.FuncAnimation(plt.gcf(), update, interval=style.animate_frame_ms, blit=True,
                                               frames=len(data_frame_list),
                                               init_func=init, repeat=True)
            except Exception as e:
                print(str(e))

        # fig.autofmt_xdate()

        try:
            style = self.generate_file_names(style, 'matplotlib')

            if style.save_fig:

                # TODO get save movie file to work in GIF and MP4 (hangs currently on these)
                # install FFMPEG with: conda install --channel https://conda.anaconda.org/conda-forge ffmpeg
                if style.animate_figure:
                    pass
                    # file = style.file_output.upper()

                    # if '.GIF' in file:
                    # anim.save(style.file_output, writer='imagemagick', fps=5, dpi=80)
                    # print('GIF saved')

                    # plt.rcParams['animation.ffmpeg_path'] = 'c:\\ffmpeg\\bin\\ffmpeg.exe'

                    # Writer = animation.writers['ffmpeg']
                    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
                    # anim.save('test.mp4', writer=writer)

                plt.savefig(style.file_output, transparent=False)
        except Exception as e:
             print(str(e))


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

        # display in matplotlib window (or clear from pyplot)
        try:
            if cc.chartfactory_silent_display == True:
                plt.close(fig)

                return fig
            elif style.silent_display == False:
                if not(style.block_new_plots):
                    # TODO
                    pass

                plt.show()
            else:
                plt.close(fig)

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
        matplotlib.rcParams.update({'font.size': matplotlib.rcParams['font.size'] * abs(style.scale_factor)})

        # do not use offsets/scientific notation
        matplotlib.rcParams.update({'axes.formatter.useoffset': False})

    def format_x_axis(self, ax, data_frame, style, has_bar, bar_ind, bar_width, has_matrix):

        if has_matrix == '2d-matrix' or has_matrix == '3d-matrix':
            x_bar_ind = np.arange(0, len(data_frame.columns))
            y_bar_ind = np.arange(0, len(data_frame.index))

            offset = 0.5
            ax.set_xticks(x_bar_ind + offset)
            ax.set_xlim([0, len(x_bar_ind)])
            ax.set_yticks(y_bar_ind + offset)
            ax.set_ylim([0, len(y_bar_ind)])

            plt.setp(plt.yticks()[1], rotation=90)

            ax.set_xticklabels(data_frame.columns, minor=False)
            ax.set_yticklabels(data_frame.index, minor=False)

            ax.plot([], [])

            for x in range(len(data_frame.index)):
                for y in range(len(data_frame.columns)):

                    plt.text(x +  offset, y +  offset, '%.0f' % data_frame.ix[x, y],
                         horizontalalignment='center',
                         verticalalignment='center',
                         )

            return

        if has_bar == 'barv':
            if matplotlib.__version__ > '1.9':
                offset = bar_width / 2.0    # for matplotlib 2
            else:
                offset = 0

            ax.set_xticks(bar_ind - offset)
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
                    myFmt = mdates.DateFormatter(style.date_formatter)

                plt.tight_layout()
                # ax.tick_params(axis='x', labelsize=matplotlib.rcParams['font.size'] * 0.5)
            return
        elif has_bar == 'barh':
            ax.set_yticks(bar_ind)
            ax.set_yticklabels(data_frame.index)
            ax.set_ylim([-1, len(bar_ind)])

            # if lots of labels make text smaller and rotate
            if len(bar_ind) > 6:
                #plt.setp(plt.yticks()[1])
                # plt.gca().tight_layout()
                # matplotlib.rcParams.update({'figure.autolayout': True})
                # plt.gcf().subplots_adjust(bottom=5)
                import matplotlib.dates as mdates

                if style.date_formatter is not None:
                    ax.format_ydata = mdates.DateFormatter(style.date_formatter)

                plt.tight_layout()
                # ax.tick_params(axis='x', labelsize=matplotlib.rcParams['font.size'] * 0.5)
            return


        # format X axis
        dates = data_frame.index

        # scaling for time series plots with hours and minutes only (and no dates)
        if hasattr(data_frame.index[0], 'hour') and not(hasattr(data_frame.index[0], 'month')):
            ax.xaxis.set_major_locator(MultipleLocator(86400./3.))
            ax.xaxis.set_minor_locator(MultipleLocator(86400./24.))
            ax.grid(b = style.x_axis_showgrid, which='minor', color='w', linewidth=0.5)

        # TODO have more refined way of formating time series x-axis!

        # scaling for time series plots with dates too
        else:
            # to handle dates
            try:
                dates = dates.to_pydatetime()
                diff = data_frame.index[-1] - data_frame.index[0]

                import matplotlib.dates as md

                if style.date_formatter is not None:
                    # from matplotlib.ticker import Formatter
                    #
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

                    ax.xaxis.set_major_formatter(md.DateFormatter(style.date_formatter))
                elif diff < timedelta(days = 4):

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
                else:
                    years = floor(diff.days/365.0/5.0)
                    locator = YearLocator(years)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))

                if matplotlib.__version__ > '1.9':
                    max = dates.max()
                    min = dates.min()

                    plt.xlim(min, max)

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

            ax.annotate(text, xy=(1, 1), xycoords='axes fraction', fontsize=8 * abs(scale_factor),
                    xytext=(-5 * abs(scale_factor), 10 * abs(scale_factor)), textcoords='offset points',
                    ha='right', va='top')

            # Plot R^2 value
            # ax.text(0.65, 0.95, text, fontsize = 10 * scale_factor,
            #            ha= 'left',
            #            va = 'top', transform = ax.transAxes)
            pass
        else:
            # return the R^2 value:
            return Rsqr

    def _create_brand_label(self, ax, anno, scale_factor):
        ax.annotate(anno, xy = (1, 1), xycoords = 'axes fraction',
                    fontsize = 10 * abs(scale_factor), color = 'white',
                    xytext = (0 * abs(scale_factor), 15 * abs(scale_factor)), textcoords = 'offset points',
                    va = "center", ha = "center",
                    bbox = dict(boxstyle = "round,pad=0.0", facecolor = cc.chartfactory_brand_color))

    def _create_subplot(self, fig, chart_type, style, subplot_no, first_ax, ordinal):

        if style.title is not None:
            fig.suptitle(style.title, fontsize = 14 * abs(style.scale_factor))

        chart_projection = '2d'

        if not (isinstance(chart_type, list)):
            if chart_type == 'surface': chart_projection = '3d'

        if style.subplots == False and first_ax is None:
            if chart_projection == '3d':
                ax = fig.add_subplot(111, projection=chart_projection)
            else:
                ax = fig.add_subplot(111)
        else:
            if first_ax is None:
                if chart_projection == '3d':
                    ax = fig.add_subplot(2, 1, subplot_no, projection=chart_projection)
                else:
                    ax = fig.add_subplot(2, 1, subplot_no)

                first_ax = ax

            if style.share_subplot_x:
                if chart_projection == '3d':
                    ax = fig.add_subplot(2, 1, subplot_no, sharex=first_ax, projection=chart_projection)
                else:
                    ax = fig.add_subplot(2, 1, subplot_no, sharex=first_ax)
            else:
                if chart_projection == '3d':
                    ax = fig.add_subplot(2, 1, subplot_no, projection=chart_projection)
                else:
                    ax = fig.add_subplot(2, 1, subplot_no)

        subplot_no = subplot_no + 1

        if style.x_title != '': ax.set_xlabel(style.x_title)
        if style.y_title != '': ax.set_ylabel(style.y_title)

        plt.xlabel(style.x_title)
        plt.ylabel(style.y_title)

        # format Y axis
        y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)

        # create a second y axis if necessary
        ax2 = []

        ax.xaxis.grid(style.x_axis_showgrid)
        ax.yaxis.grid(style.y_axis_showgrid)

        if style.y_axis_2_series != []:
            ax2 = ax.twinx()

            # set grid for second y axis
            ax2.yaxis.grid(style.y_axis_2_showgrid)

        return ax, ax2, subplot_no, ordinal + 1


    def _create_legend(self, ax, ax2, style):
        if style.display_source_label == True and style.source is not None:
            ax.annotate('Source: ' + style.source, xy=(1, 0), xycoords='axes fraction',
                        fontsize=7 * abs(style.scale_factor),
                        xytext=(-5 * abs(style.scale_factor), 10 * abs(style.scale_factor)), textcoords='offset points',
                        ha='right', va='top', color=style.source_color)

        if style.display_brand_label == True:
            self._create_brand_label(ax, anno=style.brand_label, scale_factor=abs(style.scale_factor))

        leg = []
        leg2 = []

        loc = 'best'

        # if we have two y-axis then make sure legends are in opposite corners
        if ax2 != []: loc = 2

        try:
            leg = ax.legend(loc=loc, prop={'size': 10 * abs(style.scale_factor)})
            leg.get_frame().set_linewidth(0.0)
            leg.get_frame().set_alpha(0)

            if ax2 != []:
                leg2 = ax2.legend(loc=1, prop={'size': 10 * abs(style.scale_factor)})
                leg2.get_frame().set_linewidth(0.0)
                leg2.get_frame().set_alpha(0)
        except:
            pass

        try:
            if style.display_legend is False:
                if leg != []: leg.remove()
                if leg2 != []: leg.remove()
        except:
            pass


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
            if (style.plotly_plot_mode == 'offline_html' and style.scale_factor > 0):
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
                                           dimensions=(style.width * abs(style.scale_factor) * scale,
                                                       style.height * abs(style.scale_factor) * scale),
                                           asFigure=True)

                elif chart_type_ord == 'heatmap':
                    fig = data_frame.iplot(kind=chart_type,
                                           title=style.title,
                                           xTitle=style.x_title,
                                           yTitle=style.y_title,
                                           x=x, y=y,
                                           mode=mode,
                                           size=marker_size,
                                           theme=style.plotly_theme,
                                           bestfit=style.line_of_best_fit,
                                           legend=style.display_legend,
                                           colorscale=style.color,
                                           dimensions=(style.width * abs(style.scale_factor) * scale,
                                                       style.height * abs(style.scale_factor) * scale),
                                           asFigure=True)

                    # TODO get annotations to work on Plotly/cufflinks heatmaps

                    # z = data_frame.values
                    #
                    # annotations = []
                    # for n, row in enumerate(z):
                    #     for m, val in enumerate(row):
                    #         val = z[n][m]
                    #         annotations.append(
                    #             dict(
                    #                 text=str(val),
                    #                 x=x[m], y=y[n],
                    #                 xref='x1', yref='y1',
                    #                 font=dict(color='white' if val > 0.5 else 'black'),
                    #                 showarrow=False)
                    #         )
                    #
                    # fig['layout'].update(
                    #     annotations=annotations,
                    # )

                elif chart_type_ord == 'line':
                    chart_type_ord = 'scatter'
                elif chart_type_ord == 'scatter':
                    mode = 'markers'
                    marker_size = 5
                elif chart_type_ord == 'bubble':
                    x = data_frame.columns[0]
                    y = data_frame.columns[1]
                    z = data_frame.columns[2]

                # special case for map/choropleth which has yet to be implemented in Cufflinks
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

                if chart_type_ord not in ['surface', 'choropleth', 'heatmap']:

                    fig = data_frame.iplot(kind=chart_type_ord,
                                           title=style.title,
                                           xTitle=style.x_title,
                                           yTitle=style.y_title,
                                           x=x, y=y, z=z,
                                           subplots=False,
                                           mode=mode,
                                           secondary_y=style.y_axis_2_series,
                                           size=marker_size,
                                           theme=style.plotly_theme,
                                           bestfit=style.line_of_best_fit,
                                           legend=style.display_legend,
                                           color=color_spec1,
                                           dimensions=(style.width * abs(style.scale_factor) * scale,
                                                       style.height * abs(style.scale_factor) * scale),
                                           asFigure=True)

                fig.update(dict(layout=dict(legend=dict(
                    x=0.05,
                    y=1
                ))))

                import plotly.graph_objs as go

                if style.thin_margin:
                    fig.update(dict(layout=dict(margin=go.Margin(
                        l=20,
                        r=20,
                        b=40,
                        t=40,
                        pad=0
                    ))))

                # change background color
                fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
                fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))

                # deal with grids
                if (not(style.x_axis_showgrid)): fig.update(dict(layout=dict(xaxis=dict(showgrid=style.x_axis_showgrid))))
                if (not(style.y_axis_showgrid)): fig.update(dict(layout=dict(yaxis=dict(showgrid=style.y_axis_showgrid))))
                if (not(style.y_axis_2_showgrid)): fig.update(dict(layout=dict(yaxis2=dict(showgrid=style.y_axis_2_showgrid))))

                fig_list.append(fig)

            if len(fig_list) > 1:
                import cufflinks
                fig = cufflinks.subplots(fig_list)
            else:
                fig = fig_list[0]

        self.publish_plot(fig, style)

    def publish_plot(self, fig, style):
        # change background color
        fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
        fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))

        style = self.generate_file_names(style, 'plotly')

        if style.plotly_plot_mode == 'online':
            plotly.tools.set_credentials_file(username=style.plotly_username, api_key=style.plotly_api_key)

            plotly.plotly.plot(fig, filename=style.plotly_url,
                    world_readable=style.plotly_world_readable,
                    auto_open = not(style.silent_display),
                    asImage=style.plotly_as_image)

        elif style.plotly_plot_mode == 'offline_html':
            plotly.offline.plot(fig, filename=style.html_file_output, auto_open = not(style.silent_display))

        elif style.plotly_plot_mode == 'offline_jupyter':

            # plot in IPython notebook
            plotly.offline.init_notebook_mode()
            plotly.offline.iplot(fig)

        # plotly.offline.plot(fig, filename=style.file_output, format='png',
        #         width=style.width * style.scale_factor, height=style.height * style.scale_factor)
        try:
            plotly.plotly.image.save_as(fig, filename=style.file_output, format='png',
                                width=style.width * abs(style.scale_factor), height=style.height * abs(style.scale_factor))
        except: pass

    def get_color_list(self, i):
        color_palette = cc.plotly_palette

        return color_palette[i % len(color_palette)]

#######################################################################################################################

# create color lists to be used in plots

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
