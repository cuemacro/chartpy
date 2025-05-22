from __future__ import division

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
Style

Styles for the charts to be plotted in Chart

"""

import datetime

from chartpy.chartconstants import ChartConstants

class Style(object):
    cc = ChartConstants()

    def __init__(self,
                 # Captions
                 title='',
                 x_title='',
                 y_title='',
                 y_2_title='',
                 z_title='',
                 units='',

                 font_family=cc.chartfactory_font_family,

                 # Type of plot (can be defined as list)
                 engine=None,
                 chart_type=None,

                 # Type of bar chart
                 barmode=cc.barmode,
                 stackgroup=None,

                 # Drop NaN points before plotting
                 drop_na=False,

                 # Colors
                 color=[],
                 color_2=[],
                 color_2_series=[],
                 exclude_from_color=[],
                 normalize_colormap=True,

                 # Bubble charts
                 bubble_series=None,
                 bubble_size_scalar=cc.chartfactory_bubble_size_scalar,

                 # Candlestick charts
                 candlestick_series=None,
                 candlestick_increasing_color=None,
                 candlestick_increasing_line_color=None,
                 candlestick_decreasing_color=None,
                 candlestick_decreasing_line_color=None,

                 # Overlay figures
                 overlay_fig=None,

                 # Subplot
                 subplots=False,
                 subplot_titles=None,
                 share_subplot_x=False,

                 # Display sizes
                 scale_factor=cc.chartfactory_scale_factor,
                 dpi=cc.chartfactory_dpi,
                 width=cc.chartfactory_width,
                 height=cc.chartfactory_height,
                 resample=None,
                 thin_margin=False,
                 auto_scale=cc.auto_scale,

                 # Should we block display of new screens?
                 block_new_plots=False,

                 # show this be an animation?
                 animate_figure=False,
                 animate_titles=None,
                 animate_frame_ms=250,

                 # Lines and multiple y-axis
                 y_axis_2_series=[],
                 linewidth_2_series=[],
                 linewidth=None,
                 linewidth_2=None,
                 marker_size=1,
                 line_of_best_fit=False,
                 line_shape=None,

                 # Shaded regions
                 x_shade_dates=None,

                 # Grid
                 x_axis_showgrid=True,
                 y_axis_showgrid=True,
                 y_axis_2_showgrid=True,
                 z_axis_showgrid=True,

                 # Vertical and horizontal lines from axis
                 x_y_line=[],
                 x_axis_range=None,
                 y_axis_range=None,
                 z_axis_range=None,
                 y_axis_2_range=None,

                 # Are x-axis of style category?
                 x_axis_type=None,
                 y_axis_type=None,

                 x_dtick=None,
                 y_dtick=None,

                 # Connect gaps
                 connect_line_gaps=False,

                 # Labelling of sources
                 brand_label=cc.chartfactory_brand_label,
                 display_brand_label=cc.chartfactory_display_brand_label,
                 source=cc.chartfactory_source,
                 source_color='black',
                 display_source_label=cc.chartfactory_display_source_label,
                 display_legend=True,

                 # Legend properties
                 legend_x_anchor=None,
                 legend_y_anchor=None,
                 legend_x_pos=None,
                 legend_y_pos=None,
                 legend_bgcolor=None,
                 legend_orientation=None,

                 # matplotlib only
                 xkcd=False,

                 # Display output
                 silent_display=False,
                 file_output=None,
                 date_formatter=None,

                 # Output
                 html_file_output=None,
                 display_mpld3=False,
                 auto_generate_filename=False,
                 auto_generate_html_filename=False,
                 save_fig=True,

                 # plotly only
                 plotly_url=None,
                 plotly_as_image=False,
                 plotly_username=cc.plotly_default_username,
                 plotly_api_key=None,
                 plotly_world_readable=cc.plotly_world_readable,
                 plotly_sharing=cc.plotly_sharing,
                 plotly_theme=cc.plotly_theme,
                 plotly_plot_mode=cc.plotly_plot_mode,
                 plotly_webgl=cc.plotly_webgl,
                 plotly_helper=cc.plotly_helper,

                 # Bokeh
                 bokeh_plot_mode=cc.bokeh_plot_mode,

                 # plotly choropleth fields


                 # Matplotlib only
                 style_sheet=cc.chartfactory_default_stylesheet,
                 convert_matplotlib_to_plotly=False
                 ):

        self.engine = engine

        # Captions
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.y_2_title = y_2_title
        self.z_title = z_title
        self.units = units

        self.font_family = font_family

        # Chart type
        self.chart_type = chart_type

        # Type of bar mode
        self.barmode = barmode
        self.stackgroup = stackgroup

        # Drop NaN before plotting
        self.drop_na = drop_na

        # Colors
        self.color = color
        self.color_2 = color_2
        self.color_2_series = color_2_series
        self.exclude_from_color = exclude_from_color
        self.normalize_colormap = normalize_colormap

        # Bubble specific fields
        self.bubble_series = bubble_series
        self.bubble_size_scalar = bubble_size_scalar

        # Candlestick specific fields
        self.candlestick_series = candlestick_series
        self.candlestick_increasing_color = candlestick_increasing_color
        self.candlestick_increasing_line_color = candlestick_increasing_line_color
        self.candlestick_decreasing_color = candlestick_decreasing_color
        self.candlestick_decreasing_line_color = candlestick_decreasing_line_color

        # Overlay plots
        self.overlay_fig = overlay_fig

        # Subplots
        self.subplots = subplots
        self.subplot_titles = subplot_titles
        self.share_subplot_x = share_subplot_x

        # Display sizes
        self.scale_factor = scale_factor
        self.dpi = dpi
        self.width = width
        self.height = height
        self.resample = resample
        self.thin_margin = thin_margin
        self.auto_scale = auto_scale

        # Block display
        self.block_new_plots = block_new_plots

        # Animation parameters
        self.animate_figure = animate_figure
        self.animate_titles = animate_titles
        self.animate_frame_ms = animate_frame_ms

        # Lines and multiple y-axis
        self.y_axis_2_series = y_axis_2_series
        self.linewidth_2_series = linewidth_2_series
        self.linewidth = linewidth
        self.linewidth_2 = linewidth_2
        self.marker_size = marker_size
        self.line_of_best_fit = line_of_best_fit
        self.line_shape = line_shape

        # Shaded regions
        self.x_shade_dates = x_shade_dates

        # Grids
        self.x_axis_showgrid = x_axis_showgrid
        self.y_axis_showgrid = y_axis_showgrid
        self.z_axis_showgrid = z_axis_showgrid
        self.y_axis_2_showgrid = y_axis_2_showgrid

        # Arbitrary line
        self.x_y_line = x_y_line
        self.x_axis_range = x_axis_range
        self.y_axis_range = y_axis_range
        self.y_axis_2_range = y_axis_2_range
        self.z_axis_range = z_axis_range

        # x and y axis type (eg. category)
        self.x_axis_type = x_axis_type
        self.y_axis_type = y_axis_type

        # Gaps between tick labels
        self.x_dtick = x_dtick
        self.y_dtick = y_dtick

        # Connect line gaps
        self.connect_line_gaps = connect_line_gaps

        # Labelling of sources
        self.brand_label = brand_label
        self.display_brand_label = display_brand_label
        self.source = source
        self.source_color = source_color
        self.display_source_label = display_source_label
        self.display_legend = display_legend

        # Legend Properties
        self.legend_x_anchor = legend_x_anchor
        self.legend_y_anchor = legend_y_anchor
        self.legend_x_pos = legend_x_pos
        self.legend_y_pos = legend_y_pos
        self.legend_bgcolor = legend_bgcolor
        self.legend_orientation = legend_orientation

        # matplotlib only
        self.xkcd = xkcd

        # Display output
        self.silent_display = silent_display
        self.file_output = file_output
        self.save_fig = save_fig
        self.date_formatter = date_formatter

        # Output
        self.html_file_output = html_file_output
        self.display_mpld3 = display_mpld3
        self.auto_generate_filename = auto_generate_filename
        self.auto_generate_html_filename = auto_generate_html_filename

        # bokeh only
        self.bokeh_plot_mode = bokeh_plot_mode  # 'online', 'offline_html', 'offline_jupyter'

        # plotly only
        if plotly_url is None:
            if isinstance(title, list):
                plotly_url = str(title[0])
            else:
                plotly_url = title

            plotly_url = plotly_url +  datetime.datetime.utcnow().strftime("%b-%d-%Y-%H-%M-%S")

        self.plotly_url = plotly_url
        self.plotly_as_image = plotly_as_image
        self.plotly_username = plotly_username
        self.plotly_webgl = plotly_webgl
        self.plotly_helper = plotly_helper

        # try to get API key from GraphicsConstants file
        try:
            if plotly_api_key is None: plotly_api_key = ChartConstants().plotly_creds[plotly_username]
        except:
            pass

        self.plotly_api_key = plotly_api_key
        self.plotly_world_readable = plotly_world_readable
        self.plotly_sharing = plotly_sharing
        self.plotly_theme = plotly_theme
        self.plotly_plot_mode = plotly_plot_mode  # 'dash', 'online', 'offline_html', 'offline_jupyter'

        # matplotlib only
        self.style_sheet = style_sheet
        self.convert_matplotlib_to_plotly = convert_matplotlib_to_plotly

    def str_list(self, original):

        # if is of the form pandas index
        try:
            original = original.tolist()
        except:
            pass

        if isinstance(original, list):
            original = [str(x) for x in original]

        return original

    ##### general captions
    @property
    def engine(self):
        return self.__engine

    @engine.setter
    def engine(self, engine):
        self.__engine = engine

    ##### general captions
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def x_title(self):
        return self.__x_title

    @x_title.setter
    def x_title(self, x_title):
        self.__x_title = x_title

    @property
    def y_title(self):
        return self.__y_title

    @y_title.setter
    def y_title(self, y_title):
        self.__y_title = y_title

    @property
    def y_2_title(self):
        return self.__y_2_title

    @y_2_title.setter
    def y_2_title(self, y_2_title):
        self.__y_2_title = y_2_title

    @property
    def z_title(self):
        return self.__z_title

    @y_title.setter
    def z_title(self, z_title):
        self.__z_title = z_title

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, units):
        self.__units = units

    @property
    def font_family(self):
        return self.__font_family

    @font_family.setter
    def font_family(self, font_family):
        self.__font_family = font_family

    ###### chart type
    @property
    def chart_type(self):
        return self.__chart_type

    @chart_type.setter
    def chart_type(self, chart_type):
        self.__chart_type = chart_type

    ###### barmode
    @property
    def barmode(self):
        return self.__barmode

    @barmode.setter
    def barmode(self, barmode):
        self.__barmode = barmode

    @property
    def stackgroup(self):
        return self.__stackgroup

    @stackgroup.setter
    def stackgroup(self, stackgroup):
        self.__stackgroup = stackgroup

    ###### drop na
    @property
    def drop_na(self):
        return self.__drop_na

    @drop_na.setter
    def drop_na(self, drop_na):
        self.__drop_na = drop_na

    ###### colors
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def color_2(self):
        return self.__color_2

    @color_2.setter
    def color_2(self, color_2):
        self.__color_2 = color_2

    @property
    def color_2_series(self):
        return self.__color_2_series

    @color_2_series.setter
    def color_2_series(self, color_2_series):
        self.__color_2_series = self.str_list(color_2_series)

    @property
    def exclude_from_color(self):
        return self.__exclude_from_color

    @exclude_from_color.setter
    def exclude_from_color(self, exclude_from_color):
        self.__exclude_from_color = self.str_list(exclude_from_color)

    @property
    def normalize_colormap(self):
        return self.__normalize_colormap

    @normalize_colormap.setter
    def normalize_colormap(self, normalize_colormap):
        self.__normalize_colormap = self.str_list(normalize_colormap)

    ###### bubble specific series

    @property
    def bubble_series(self):
        return self.__bubble_series

    @bubble_series.setter
    def bubble_series(self, bubble_series):
        self.__bubble_series = self.str_list(bubble_series)

    @property
    def bubble_size_scalar(self):
        return self.__bubble_size_scalar

    @bubble_size_scalar.setter
    def bubble_size_scalar(self, bubble_size_scalar):
        self.__bubble_size_scalar = bubble_size_scalar

    ###### candlestick specific series
    @property
    def candlestick_series(self):
        return self.__candlestick_series

    @candlestick_series.setter
    def candlestick_series(self, candlestick_series):
        self.__candlestick_series = self.str_list(candlestick_series)

    @property
    def candlestick_increasing_color(self):
        return self.__candlestick_increasing_color

    @candlestick_increasing_color.setter
    def candlestick_increasing_color(self, candlestick_increasing_color):
        self.__candlestick_increasing_color = candlestick_increasing_color

    @property
    def candlestick_increasing_line_color(self):
        return self.__candlestick_increasing_line_color

    @candlestick_increasing_line_color.setter
    def candlestick_increasing_line_color(self, candlestick_increasing_line_color):
        self.__candlestick_increasing_line_color = candlestick_increasing_line_color

    @property
    def candlestick_decreasing_color(self):
        return self.__candlestick_decreasing_color

    @candlestick_decreasing_color.setter
    def candlestick_decreasing_color(self, candlestick_decreasing_color):
        self.__candlestick_decreasing_color = candlestick_decreasing_color

    @property
    def candlestick_decreasing_line_color(self):
        return self.__candlestick_decreasing_line_color

    @candlestick_decreasing_line_color.setter
    def candlestick_decreasing_line_color(self, candlestick_decreasing_line_color):
        self.__candlestick_decreasing_line_color = candlestick_decreasing_line_color

    ###### Overlay figures
    @property
    def overlay_fig(self):
        return self.__overlay_fig

    @overlay_fig.setter
    def overlay_fig(self, overlay_fig):
        self.__overlay_fig = overlay_fig

    ###### Subplots
    @property
    def subplots(self):
        return self.__subplots

    @subplots.setter
    def subplots(self, subplots):
        self.__subplots = subplots

    @property
    def subplot_titles(self):
        return self.__subplot_titles

    @subplot_titles.setter
    def subplot_titles(self, subplot_titles):
        self.__subplot_titles = subplot_titles


    @property
    def share_subplot_x(self):
        return self.__share_subplot_x

    @share_subplot_x.setter
    def share_subplot_x(self, share_subplot_x):
        self.__share_subplot_x = share_subplot_x

    ###### chart size
    @property
    def scale_factor(self):
        return self.__scale_factor

    @scale_factor.setter
    def scale_factor(self, scale_factor):
        self.__scale_factor = scale_factor

    @property
    def auto_scale(self):
        return self.__auto_scale

    @auto_scale.setter
    def auto_scale(self, auto_scale):
        self.__auto_scale = auto_scale

    @property
    def dpi(self):
        return self.__dpi

    @dpi.setter
    def dpi(self, dpi):
        self.__dpi = dpi

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def thin_margin(self):
        return self.__thin_margin

    @thin_margin.setter
    def thin_margin(self, thin_margin):
        self.__thin_margin = thin_margin

    @property
    def block_new_plots(self):
        return self.__block_new_plots

    @block_new_plots.setter
    def block_new_plots(self, block_new_plots):
        self.__block_new_plots = block_new_plots

    @property
    def animate_figure(self):
        return self.__animate_figure

    @animate_figure.setter
    def animate_figure(self, animate_figure):
        self.__animate_figure = animate_figure

    @property
    def animate_titles(self):
        return self.__animate_titles

    @animate_titles.setter
    def animate_titles(self, animate_titles):
        self.__animate_titles = animate_titles

    @property
    def animate_frame_ms(self):
        return self.__animate_frame_ms

    @animate_frame_ms.setter
    def animate_frame_ms(self, animate_frame_ms):
        self.__animate_frame_ms = animate_frame_ms


    ###### resample frequency
    @property
    def resample(self):
        return self.__resample

    @resample.setter
    def resample(self, resample):
        self.__resample = resample

    ###### line properties and second y-axis
    @property
    def y_axis_2_series(self):
        return self.__y_axis_2_series

    @y_axis_2_series.setter
    def y_axis_2_series(self, y_axis_2_series):
        self.__y_axis_2_series = self.str_list(y_axis_2_series)

    @property
    def linewidth_2_series(self):
        return self.__linewidth_2_series

    @linewidth_2_series.setter
    def linewidth_2_series(self, linewidth_2_series):
        self.__linewidth_2_series = self.str_list(linewidth_2_series)

    @property
    def linewidth(self):
        return self.__linewidth

    @linewidth.setter
    def linewidth(self, linewidth):
        self.__linewidth = linewidth

    @property
    def linewidth_2(self):
        return self.__linewidth_2

    @linewidth_2.setter
    def linewidth_2(self, linewidth_2):
        self.__linewidth_2 = linewidth_2

    @property
    def marker_size(self):
        return self.__marker_size

    @marker_size.setter
    def marker_size(self, marker_size):
        self.__marker_size = marker_size

    @property
    def line_of_best_fit(self):
        return self.__line_of_best_fit

    @line_of_best_fit.setter
    def line_of_best_fit(self, line_of_best_fit):
        self.__line_of_best_fit = line_of_best_fit

    @property
    def line_shape(self):
        return self.__line_shape

    @line_shape.setter
    def line_shape(self, line_shape):
        self.__line_shape = line_shape


    ###### Shaded regions

    @property
    def x_shade_dates(self):
        return self.__x_shade_dates

    @x_shade_dates.setter
    def x_shade_dates(self, x_shade_dates):
        self.__x_shade_dates = x_shade_dates

    ###### Grids
    @property
    def x_axis_showgrid(self):
        return self.__x_axis_showgrid

    @x_axis_showgrid.setter
    def x_axis_showgrid(self, x_axis_showgrid):
        self.__x_axis_showgrid = x_axis_showgrid

    @property
    def y_axis_showgrid(self):
        return self.__y_axis_showgrid

    @y_axis_showgrid.setter
    def y_axis_showgrid(self, y_axis_showgrid):
        self.__y_axis_showgrid = y_axis_showgrid

    @property
    def z_axis_showgrid(self):
        return self.__z_axis_showgrid

    @z_axis_showgrid.setter
    def z_axis_showgrid(self, z_axis_showgrid):
        self.__z_axis_showgrid = z_axis_showgrid

    @property
    def y_axis_2_showgrid(self):
        return self.__y_axis_2_showgrid

    @y_axis_2_showgrid.setter
    def y_axis_2_showgrid(self, y_axis_2_showgrid):
        self.__y_axis_2_showgrid = y_axis_2_showgrid

    ###### vertical and horizontal lines
    @property
    def x_y_line(self):
        return self.__x_y_line

    @x_y_line.setter
    def x_y_line(self, x_y_line):
        self.__x_y_line = x_y_line

    @property
    def x_axis_range(self):
        return self.__x_axis_range

    @x_axis_range.setter
    def x_axis_range(self, x_axis_range):
        self.__x_axis_range = x_axis_range

    @property
    def y_axis_range(self):
        return self.__y_axis_range

    @y_axis_range.setter
    def y_axis_range(self, y_axis_range):
        self.__y_axis_range = y_axis_range

    @property
    def y_axis_2_range(self):
        return self.__y_axis_2_range

    @y_axis_2_range.setter
    def y_axis_2_range(self, y_axis_2_range):
        self.__y_axis_2_range = y_axis_2_range

    @property
    def z_axis_range(self):
        return self.__z_axis_range

    @z_axis_range.setter
    def z_axis_range(self, z_axis_range):
        self.__z_axis_range = z_axis_range

    ###### axis type

    @property
    def x_axis_type(self):
        return self.__x_axis_type

    @x_axis_type.setter
    def x_axis_type(self, x_axis_type):
        self.__x_axis_type = x_axis_type

    @property
    def y_axis_type(self):
        return self.__y_axis_type

    @y_axis_type.setter
    def y_axis_type(self, y_axis_type):
        self.__y_axis_type = y_axis_type

    ###### gaps between tick labels
    @property
    def x_dtick(self):
        return self.__x_dtick

    @x_dtick.setter
    def x_dtick(self, x_dtick):
        self.__x_dtick = x_dtick

    @property
    def y_dtick(self):
        return self.__y_dtick

    @y_dtick.setter
    def y_dtick(self, y_dtick):
        self.__y_dtick = y_dtick

    ###### connect line gaps
    @property
    def connect_line_gaps(self):
        return self.__connect_line_gaps

    @connect_line_gaps.setter
    def connect_line_gaps(self, connect_line_gaps):
        self.__connect_line_gaps = connect_line_gaps


    ###### label properties
    @property
    def brand_label(self):
        return self.__brand_label

    @brand_label.setter
    def brand_label(self, brand_label):
        self.__brand_label = brand_label

    @property
    def display_brand_label(self):
        return self.__display_brand_label

    @display_brand_label.setter
    def display_brand_label(self, display_brand_label):
        self.__display_brand_label = display_brand_label

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        self.__source = source

    @property
    def source(self):
        return self.__source_color

    @source.setter
    def source(self, source_color):
        self.__source_color = source_color

    @property
    def display_source_label(self):
        return self.__display_source_label

    @display_source_label.setter
    def display_source_label(self, display_source_label):
        self.__display_source_label = display_source_label

    @property
    def display_legend(self):
        return self.__display_legend

    @display_legend.setter
    def display_legend(self, display_legend):
        self.__display_legend = display_legend

    ###### Legend properties

    @property
    def legend_x_anchor(self):
        return self.__legend_x_anchor

    @legend_x_anchor.setter
    def legend_x_anchor(self, legend_x_anchor):
        self.__legend_x_anchor = legend_x_anchor

    @property
    def legend_y_anchor(self):
        return self.__legend_y_anchor

    @legend_y_anchor.setter
    def legend_y_anchor(self, legend_y_anchor):
        self.__legend_y_anchor = legend_y_anchor

    @property
    def legend_x_pos(self):
        return self.__legend_x_pos

    @legend_x_pos.setter
    def legend_x_pos(self, legend_x_pos):
        self.__legend_x_pos = legend_x_pos

    @property
    def legend_y_pos(self):
        return self.__legend_y_pos

    @legend_y_pos.setter
    def legend_y_pos(self, legend_y_pos):
        self.__legend_y_pos = legend_y_pos

    @property
    def legend_bgcolor(self):
        return self.__legend_bgcolor

    @legend_bgcolor.setter
    def legend_bgcolor(self, legend_bgcolor):
        self.__legend_bgcolor = legend_bgcolor

    @property
    def legend_orientation(self):
        return self.__legend_orientation

    @legend_orientation.setter
    def legend_orientation(self, legend_orientation):
        self.__legend_orientation = legend_orientation

    ###### matplotlib only
    @property
    def xkcd(self):
        return self.__xkcd

    @xkcd.setter
    def xkcd(self, xkcd):
        self.__xkcd = xkcd

    ###### display output settings
    @property
    def silent_display(self):
        return self.__silent_display

    @silent_display.setter
    def silent_display(self, silent_display):
        self.__silent_display = silent_display

    @property
    def file_output(self):
        return self.__file_output

    @file_output.setter
    def file_output(self, file_output):
        self.__file_output = file_output

    @property
    def save_fig(self):
        return self.__save_fig

    @save_fig.setter
    def save_fig(self, save_fig):
        self.__save_fig = save_fig

    @property
    def date_formatter(self):
        return self.__date_formatter

    @date_formatter.setter
    def date_formatter(self, date_formatter):
        self.__date_formatter = date_formatter

    ###### settings for MPLD3 and HTML output
    @property
    def html_file_output(self):
        return self.__html_file_output

    @html_file_output.setter
    def html_file_output(self, html_file_output):
        self.__html_file_output = html_file_output

    @property
    def display_mpld3(self):
        return self.__display_mpld3

    @display_mpld3.setter
    def display_mpld3(self, display_mpld3):
        self.__display_mpld3 = display_mpld3

    @property
    def auto_generate_filename(self):
        return self.__auto_generate_filename

    @auto_generate_filename.setter
    def auto_generate_filename(self, auto_generate_filename):
        self.__auto_generate_filename = auto_generate_filename

    @property
    def auto_generate_html_filename(self):
        return self.__auto_generate_html_filename

    @auto_generate_html_filename.setter
    def auto_generate_html_filename(self, auto_generate_html_filename):
        self.__auto_generate_html_filename = auto_generate_html_filename

    ###### Plotly specific settings
    @property
    def plotly_url(self):
        return self.__plotly_url

    @plotly_url.setter
    def plotly_url(self, plotly_url):
        self.__plotly_url = plotly_url

    @property
    def plotly_as_image(self):
        return self.__plotly_as_image

    @plotly_as_image.setter
    def plotly_as_image(self, plotly_as_image):
        self.__plotly_as_image = plotly_as_image

    @property
    def plotly_username(self):
        return self.__plotly_username

    @plotly_username.setter
    def plotly_username(self, plotly_username):
        self.__plotly_username = plotly_username
        try:
            self.plotly_api_key = ChartConstants().plotly_creds[plotly_username]
        except:
            pass

    @property
    def plotly_api_key(self):
        return self.__plotly_api_key

    @plotly_api_key.setter
    def plotly_api_key(self, plotly_api_key):
        self.__plotly_api_key = plotly_api_key

    @property
    def plotly_world_readable(self):
        return self.__plotly_world_readable

    @plotly_world_readable.setter
    def plotly_world_readable(self, plotly_world_readable):
        self.__plotly_world_readable = plotly_world_readable

    @property
    def plotly_sharing(self):
        return self.__plotly_sharing

    @plotly_sharing.setter
    def plotly_sharing(self, plotly_sharing):
        self.__plotly_sharing = plotly_sharing

    @property
    def plotly_theme(self):
        return self.__plotly_theme

    @plotly_theme.setter
    def plotly_theme(self, plotly_theme):
        self.__plotly_theme = plotly_theme

    @property
    def plotly_plot_mode(self):
        return self.__plotly_plot_mode

    @plotly_plot_mode.setter
    def plotly_plot_mode(self, plotly_plot_mode):
        self.__plotly_plot_mode = plotly_plot_mode

    @property
    def plotly_webgl(self):
        return self.__plotly_webgl

    @plotly_webgl.setter
    def plotly_webgl(self, plotly_webgl):
        self.__plotly_webgl = plotly_webgl

    @property
    def plotly_helper(self):
        return self.__plotly_helper

    @plotly_helper.setter
    def plotly_helper(self, plotly_helper):
        self.__plotly_helper = plotly_helper

    ###### bokeh specific settings
    @property
    def bokeh_plot_mode(self):
        return self.__bokeh_plot_mode

    @bokeh_plot_mode.setter
    def bokeh_plot_mode(self, bokeh_plot_mode):
        self.__bokeh_plot_mode = bokeh_plot_mode

    ###### matplotlib specific settings
    @property
    def style_sheet(self):
        return self.__style_sheet

    @style_sheet.setter
    def style_sheet(self, style_sheet):
        self.__style_sheet = style_sheet

    @property
    def convert_matplotlib_to_plotly(self):
        return self.__convert_matplotlib_to_plotly

    @convert_matplotlib_to_plotly.setter
    def convert_matplotlib_to_plotly(self, convert_matplotlib_to_plotly):
        self.__convert_matplotlib_to_plotly = convert_matplotlib_to_plotly
