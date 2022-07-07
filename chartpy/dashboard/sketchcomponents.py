__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2021 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#

## web server components
try:
    # Newer versions of Dash
    from dash import dcc
    from dash import html

    from dash import dash_table as dt
except:
    # Older versions of dash
    import dash_core_components as dcc
    import dash_html_components as html

    import dash_table as dt

## time/date components
import datetime
from datetime import timedelta


class SketchComponents(object):
    """This creates the various Dash objects, such as buttons, tables etc. that can be used to create a web dashboard.
    Abstracts away some of the complexity of creating Dash objects, by allowing us to quickly specify things like the id
    of the object, the associated page name etc.

    """

    def __init__(self, app, constants, url_prefix=''):
        self._constants = constants
        self._app = app

        self._url_prefix = url_prefix

        # Read these from constants
        self._width = 1000

        self._logo_width = 100
        self._logo_height = 100

        self._link_bar_width = self._width - 20
        self._drop_down_width = 155
        self._inputbox_width = 155
        self._date_picker_width = 155
        self._download_width = self._width - 20
        self._timeline_width = self._width - 20
        self._markdown_width = 1000
        self._table_width = 1000
        self._file_link_width = self._width - 20

        self._plot_width = 1000
        self._plot_height = 1000
        self._uploadbox_width = self._width - 20
        self._button_width = 155

    def header_bar(self, title, img=None, description=None, id=None,
                   prefix_id='', width=None, logo_height=None, logo_width=None,
                   img_full_path=None, font_family="open sans"):
        """Creates HTML for the header bar

        Parameters
        ----------
        title : str
            Title of the header

        width : int
            Width of the header bar

        logo_height : int
            Logo height

        logo_width : int
            Logo width

        Returns
        -------
        html.Div
        """

        if width is None: width = self._width
        if logo_height is None: logo_height = self._logo_height
        if logo_width is None: logo_width = self._logo_width

        div_list = [html.H2(title, className='eight columns')]

        if img is not None or img_full_path is not None:
            if img_full_path is None:
                img_full_path = self._app.get_asset_url(img)

            div_list.append(html.Img(src=img_full_path,
                                     style={'height': str(logo_height) + 'px',
                                            'width': str(logo_width) + 'px',
                                            'float': 'right'}))

        if prefix_id != '':
            prefix_id = prefix_id + '-'

        if description is not None and id is not None:
            if not (isinstance(description, list)):
                description = [description]

            if isinstance(id, str):
                id = [id]

            for id_, d in zip(id, description):
                div_list.append(html.Div(html.P(d, id=prefix_id + id_),
                                         style={'height': '20px',
                                                'width': '900px',
                                                'float': 'left',
                                                'font-family': font_family}))

        return html.Div(div_list,
                        style={'width': str(width) + 'px', 'marginBottom': 0,
                               'marginTop': 5, 'marginLeft': 5,
                               'marginRight': 5})

    def button(self, caption=None, id=None, prefix_id='', className=None,
               upload=False, button_width=None, width=None):
        """Creates an HTML button

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        className: str (default: None)
            CSS class to use for formatting

        upload : bool
            Is this an upload button?

        Returns
        -------
        html.Div
        """
        if width is None: width = self._width
        if button_width is None: button_width = self._button_width

        if prefix_id != '':
            id = prefix_id + '-' + id

        if className is None:
            button = html.Button(caption, id=id, n_clicks=0)

            if upload:
                button = dcc.Upload(button)

            return html.Div([
                button
            ], style={'width': str(button_width) + 'px',
                      'display': 'inline-block', 'marginBottom': 0,
                      'marginTop': 0, 'marginLeft': 5,
                      'marginRight': 5})

        else:
            button = html.Button(caption, id=id, n_clicks=0,
                                 className=className)

            if upload:
                button = dcc.Upload(button)

            return html.Div([
                button, " "
            ], style={'width': str(width) + 'px', 'display': 'inline-block',
                      'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5,
                      'marginRight': 5})

    def uploadbox(self, caption=None, id=None, prefix_id='', className=None,
                  width=None):
        """Creates an HTML button

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        className: str (default: None)
            CSS class to use for formatting

        upload : bool
            Is this an upload button?

        Returns
        -------
        html.Div
        """

        if width is None: width = self._uploadbox_width

        if prefix_id != '':
            id = prefix_id + '-' + id

        area = dcc.Upload(id=id, children=html.Div(
            [caption + ': Drag and Drop or ', html.A('Select Files')],
            style={'borderWidth': '1px', 'width': '980px',
                   'borderStyle': 'dashed', 'borderRadius': '5px'}))

        if className is None:

            return html.Div([
                area
            ], style={'width': str(width) + 'px', 'display': 'inline-block',
                      'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5,
                      'marginRight': 5})

        else:
            area = dcc.Upload(id=id, children=html.Div(
                ['Drag and Drop or ', html.A('Select Files')]))

            return html.Div([
                area, " "
            ], style={'width': str(width) + 'px', 'display': 'inline-block',
                      'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5,
                      'marginRight': 5})

    def plot(self, caption=None, id=None, prefix_id='', figure=None,
             element_add=None, downloadplot_caption=None,
             downloadplot_tag=None, download_file=None, width=None,
             height=None, wrap_in_div=True):
        """Creates a Plotly plot object (Dash component)

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        element_add : HTML component (default: None)
            Add this HTML component at the start

        downloadplot_caption : str (default: None)
            Caption for the download CSV

        downloadplot_tag : str (default: None)
            Tag for the download plot object

        download_file : str
            Download file name

        Returns
        -------
        html.Div
        """
        if width is None: width = self._plot_width
        if height is None: height = self._plot_height

        if prefix_id != '':
            prefix_id = prefix_id + '-'

        html_tags = []

        if caption is not None:
            html_tags.append(html.H4(caption))

        if element_add is not None:
            html_tags.append(element_add)

        if isinstance(id, str):
            id = [id]

        if figure is not None:
            if not (isinstance(figure, list)):
                figure = [figure]

        # config={'editable': True, 'modeBarButtonsToRemove': ['sendDataToCloud']

        if figure is not None:
            for id_, fig_ in zip(id, figure):

                if fig_ is None:
                    fig_ = {}

                html_tags.append(html.Div([
                    dcc.Graph(id=prefix_id + id_,
                              figure=fig_,
                              style={'width': str(width) + 'px',
                                     'height': str(height) + 'px'})
                    # , config={'modeBarButtonsToRemove': ['sendDataToCloud']})
                ]))
        else:
            for id_ in id:
                html_tags.append(html.Div([
                    dcc.Graph(figure={}, id=prefix_id + id_,
                              style={'width': str(width) + 'px',
                                     'height': str(height) + 'px'})
                    # , config={'modeBarButtonsToRemove': ['sendDataToCloud']})
                ]))

        html_style = {'width': str(width) + 'px',
                      'height': str((height * len(id)) + 100) + 'px',
                      'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5,
                      'marginRight': 5}

        html_tags = self.download_file_link(html_tags, prefix_id,
                                            downloadplot_caption,
                                            downloadplot_tag, download_file)

        if wrap_in_div:
            return html.Div(html_tags, style=html_style)

        return html_tags

    def download_file_link(self, html_tags, prefix_id,
                           downloadplot_caption_list, downloadplot_tag_list,
                           download_file_list,
                           width=None):
        """Creates links for downloading CSV files (typically associated with plots and tables)

        Parameters
        ----------
        html_tags : list
            List for the HTML tags to be appended to

        prefix_id : str
            Prefix ID with this

        downloadplot_caption_list : str (list)
            List of captions for each download

        downloadplot_tag_list : str (list)
            List of IDs for the tags

        download_file_list : str (list)
            Download file list

        Returns
        -------
        html.Div (list)
        """
        if width is None: width = self._download_width

        if html_tags is None:
            html_tags = []

        if downloadplot_caption_list != None and \
                downloadplot_tag_list != None and download_file_list != None:

            if not (isinstance(downloadplot_caption_list, list)):
                downloadplot_caption_list = [downloadplot_caption_list]

            if not (isinstance(downloadplot_tag_list, list)):
                downloadplot_tag_list = [downloadplot_tag_list]

            if not (isinstance(download_file_list, list)):
                download_file_list = [download_file_list]

            for i in range(0, len(download_file_list)):
                html_download = html.Div([
                    html.A(
                        downloadplot_caption_list[i],
                        id=prefix_id + downloadplot_tag_list[i],
                        download=download_file_list[i],
                        href="",
                        target="_blank"
                    ),
                ], style={'width': str(width) + 'px',
                          'display': 'inline-block', 'marginBottom': 0,
                          'marginTop': 0, 'marginLeft': 5,
                          'marginRight': 5, 'className': 'row'})

                html_tags.append(html_download)

        return html_tags

    def table(self, caption=None, id=None, prefix_id='', element_add=None,
              columns=None, downloadplot_caption=None,
              downloadplot_tag=None, download_file=None, width=None,
              font_size=14, font_family='open sans'):
        """

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        element_add : HTML component (default: None)
            Add this HTML component at the start

        columns : str (list)
            Column headers

        downloadplot_caption : str (default: None)
            Caption for the download CSV

        downloadplot_tag : str (default: None)
            Tag for the download plot object

        download_file : str
            Download file name

        Returns
        -------
        html.Div
        """
        if width is None: width = self._table_width

        if prefix_id != '':
            prefix_id = prefix_id + '-'

        html_tags = []
        html_tags.append(html.H3(caption))

        if element_add is not None:
            html_tags.append(element_add)

        if isinstance(id, str):
            id = [id]

        is_dash_table = True

        try:
            is_dash_table = self._constants.gui_table_type == 'dash'
        except:
            pass

        for i in range(0, len(id)):

            id_ = id[i]

            if i == len(id) - 1:
                line_break = None
            else:
                line_break = html.Br()

            if columns is None:

                if is_dash_table:
                    data_table = dt.DataTable(
                        # data=[{}],
                        # row_selectable='single',
                        # columns=[{"name": [], "id": []}],
                        sort_action="native",
                        sort_mode="multi",
                        selected_columns=[],
                        selected_rows=[],
                        style_cell={'fontSize': font_size,
                                    'font-family': font_family},
                        id=prefix_id + id_
                    )
                else:
                    data_table = html.Div([
                        html.Div(id=prefix_id + id_)
                        # , config={'modeBarButtonsToRemove': ['sendDataToCloud']})
                    ])
            else:
                col = columns

                if isinstance(columns, dict):
                    col = columns[id_]

                if is_dash_table:
                    data_table = dt.DataTable(
                        # data=[{}],
                        # row_selectable='single',
                        # columns=[{"name": i, "id": i} for i in col],
                        filtering=True,
                        sorting=True,
                        selected_rows=[],
                        id=prefix_id + id_
                    )
                else:
                    data_table = html.Div([
                        html.Div(id=prefix_id + id_)
                        # , config={'modeBarButtonsToRemove': ['sendDataToCloud']})
                    ])

            html_tags.append(html.Div([
                # html.Div(id=prefix_id + id_)
                data_table,
                line_break

                # , config={'modeBarButtonsToRemove': ['sendDataToCloud']})
            ]))

        html_tags = self.download_file_link(html_tags, prefix_id,
                                            downloadplot_caption,
                                            downloadplot_tag, download_file)

        html_style = {'width': str(width) + 'px', 'display': 'inline-block',
                      'marginBottom': 5, 'marginTop': 5, 'marginLeft': 5,
                      'marginRight': 5}

        return html.Div(html_tags, style=html_style)

    def tabs(self, layout, id='tabs-with-classes',
             parent_className='custom-tabs',
             container_className='custom-tabs-container',
             tab_className='custom-tab',
             tab_selected_className='custom-tab--selected'):

        if not (isinstance(layout, list)):
            layout = [layout]

        tab_names = []
        tab_value = []
        children = []
        layout_dict = {}

        # Create a tab for each layout object
        for lay in layout:
            tab_names.append(lay.page_name())

            tab_value_ = lay.page_name().lower().replace(' ', '-')

            tab_value.append(tab_value_)

            children.append(dcc.Tab(label=lay.page_name(),
                                    value=tab_value_,
                                    className=tab_className,
                                    selected_className=tab_selected_className))

            layout_dict[tab_value_] = lay  # .construct_layout()

        # Create tab container
        dcc_tabs = dcc.Tabs(
            id=id,
            value=tab_value[0],
            parent_className=parent_className,
            className=container_className,
            children=children)

        return dcc_tabs, tab_names, layout_dict

    def horizontal_bar(self):
        """A horizontal HTML bar

        Returns
        -------
        html.Div
        """
        # horizonal bar
        return self.width_row_cell(html.Hr())

    def row_cell(self, html_obj, id=None, prefix_id=''):
        """Wraps around an HTML object to create a table without any specific formatting

        Parameters
        ----------
        html_obj : HTML
            HTML object to be wrapped around

        Returns
        -------
        html.Div
        """
        # create a whole width table cell

        if id is not None:
            if prefix_id != '':
                id = prefix_id + '-' + id

            return html.Div(id=id)

        if not (isinstance(html_obj, list)):
            html_obj = [html_obj]

        return html.Div(html_obj)

    def width_row_cell(self, html_obj, id=None, prefix_id='', margin_left=0,
                       width=1000):
        """Wraps around an HTML object to create a wide table

        Parameters
        ----------
        html_obj : HTML
            HTML object to be wrapped around

        margin_left : int (default: 0)
            Margin of HTML

        Returns
        -------
        html.Div
        """
        # create a whole width table cell
        if width is None: width = self._width

        if id is not None:
            if prefix_id != '':
                id = prefix_id + '-' + id

            return html.Div(
                id=id,
                style={'width': str(width) + 'px', 'display': 'inline-block',
                       'marginBottom': 5, 'marginTop': 5,
                       'marginLeft': margin_left,
                       'marginRight': 0, 'className': 'row'})

        if not (isinstance(html_obj, list)):
            html_obj = [html_obj]

        return html.Div(
            html_obj,
            style={'width': str(width) + 'px', 'display': 'inline-block',
                   'marginBottom': 5, 'marginTop': 5,
                   'marginLeft': margin_left,
                   'marginRight': 0, 'className': 'row'})

    def extra_width_row_cell(self, html_obj, id=None, prefix_id='',
                             width=None):

        if width is None: width = self._width

        # Creates drop down style HTML controls
        if id is not None:
            if prefix_id != '':
                id = prefix_id + '-' + id

            return html.Div(id=id,
                            style={'width': str(width) + 'px',
                                   'display': 'inline-block',
                                   'marginBottom': 5,
                                   'marginTop': 5, 'marginLeft': 20,
                                   'marginRight': 20})

        if not (isinstance(html_obj, list)):
            html_obj = [html_obj]

        return html.Div(html_obj,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 5,
                               'marginTop': 5, 'marginLeft': 20,
                               'marginRight': 20})

    def link_bar(self, labels_links_dict, add=None, width=None):
        """Creates an link bar of Dash components, typically used as a menu on the top of a Dash based web page.

        Parameters
        ----------
        labels_links_dict : dict
            Dictionary containing labels and links to be used

        add : HTML (default: None)
            HTML object to be appended

        Returns
        -------
        html.Div
        """
        if width is None: width = self._link_bar_width

        # Creates a link bar
        key_list = self.dict_key_list(labels_links_dict.keys())

        if self._url_prefix == '':
            url_prefix = '/'
        else:
            url_prefix = '/' + self._url_prefix + '/'

        if len(labels_links_dict) == 1:
            list = [dcc.Link(key_list[0], href=url_prefix)]

        elif len(labels_links_dict) == 2:
            list = [dcc.Link(key_list[0],
                             href=url_prefix + labels_links_dict[key_list[0]]),
                    ' / ',
                    dcc.Link(key_list[1],
                             href=url_prefix + labels_links_dict[key_list[1]])]
        else:
            list = [dcc.Link(key_list[0], href=url_prefix), ' / ', ]

            for i in range(1, len(labels_links_dict) - 1):
                list.append(dcc.Link(key_list[i],
                                     href=url_prefix + labels_links_dict[
                                         key_list[i]]))
                list.append(' / ')

            list.append(list.append(
                dcc.Link(key_list[-1],
                         href=url_prefix + labels_links_dict[key_list[-1]])))

        if add is not None:
            list.append(add)

        return html.Div(list,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 5,
                               'marginTop': 5,
                               'marginLeft': 5,
                               'marginRight': 5, 'className': 'row'})

    def drop_down(self, caption=None, id=None, prefix_id='',
                  drop_down_values=None, multiselect=False, width=None,
                  multiselect_start_values=None, start_values_index=0,
                  clearable=False):
        """Creates a Dash drop down object, wrapped in HTML table

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (list) (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        drop_down_values : str (list) (default: None)
            List of drop down values

        multiselect : bool (default: False)
            Can we select multiple values?

        width : int (default: 155)
            Width of the object to display

        multiselect_start_values : str (default: None)
            Which elements to select at the start

        Returns
        -------
        html.Div
        """
        if width is None: width = self._drop_down_width

        # Creates drop down style HTML controls
        if prefix_id != '':
            prefix_id = prefix_id + '-'

        drop_list = []

        # For each ID assign the drop down values
        if isinstance(id, str):
            id = {id: drop_down_values}

        elif isinstance(id, list):
            id_list = id

            id = {}

            for i in id_list:
                id[i] = drop_down_values

        if caption is not None:
            drop_list = [html.P(caption)]

        # for each ID create a drop down object
        for key in self.dict_key_list(id.keys()):

            if multiselect_start_values is None:
                start_values = id[key][start_values_index]
            else:
                start_values = multiselect_start_values

            # each drop down as the same drop down values
            drop_list.append(dcc.Dropdown(
                id=prefix_id + key,
                options=[{'label': j, 'value': j} for j in id[key]],
                value=start_values,
                multi=multiselect,
                clearable=clearable
            ))

        # wrap it into an HTML Div style table
        return html.Div(drop_list,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 0,
                               'marginTop': 0,
                               'marginLeft': 5,
                               'marginRight': 5})

    def timeline_dropdown(self, prefix, available_plot_lines, width=None):
        """Create a dropdown for timelines (with multiple selectable values)

        Parameters
        ----------
        prefix : str

        available_plot_lines : str (list)

        Returns
        -------
        html.Div
        """
        if width is None: width = self._drop_down_width

        return html.Div([
            self.drop_down(caption=None, id=prefix + '-lines-val',
                           drop_down_values=available_plot_lines,
                           multiselect=True,
                           multiselect_start_values=available_plot_lines,
                           width=width)
        ])

    def inputbox(self, caption=None, id=None, prefix_id='', width=None,
                 start_values=None):
        """Creates a Dash input box, wrapped in HTML table

        Parameters
        ----------
        caption : str (default: None)
            Caption for the HTML object

        id : str (list) (default: None)
            ID for the HTML object

        prefix_id : str (default:'')
            Prefix to use for the ID

        start_values : str (default: None)
            Which elements to select at the start

        Returns
        -------
        html.Div
        """
        if width is None: width = self._inputbox_width

        # creates drop down style HTML controls
        if prefix_id != '':
            prefix_id = prefix_id + '-'

        text_list = []

        # For each ID assign the drop down values
        if isinstance(id, str):
            id = {id: start_values}

        elif isinstance(id, list):
            id_list = id

            id = {}

            if isinstance(start_values, list):
                for i, s in zip(id_list, start_values):
                    id[i] = s
            else:
                for i in id_list:
                    id[i] = start_values

        if caption is not None:
            text_list = [html.P(caption)]

        # for each ID create a text object
        for key in self.dict_key_list(id.keys()):
            # if start_values is not None:
            #    start_values = multiselect_start_values

            # each drop down as the same drop down values
            text_list.append(dcc.Input(
                id=prefix_id + key,
                value=id[key],
                style={'width': str(width) + 'px'}
            ))

        # wrap it into an HTML Div style table
        return html.Div(text_list,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 0,
                               'marginTop': 0,
                               'marginLeft': 5,
                               'marginRight': 5})

    def date_picker(self, caption=None, id=None, prefix_id='',
                    initial_date=datetime.date.today(), offset=None,
                    width=None):
        if width is None: width = self._date_picker_width

        if isinstance(id, str):
            id = [id]

        date_picker_list = [html.P(caption)]

        if prefix_id != '':
            prefix_id = prefix_id + '-'

        for i in range(0, len(id)):

            id_ = id[i]

            offset_ = 0
            if offset is not None:
                offset_ = offset[i]

            # date_picker_list.append(dcc.Input(
            #     id=prefix_id + id_,
            #     type='date',
            #     value=datetime.date.today() - datetime.timedelta(days=60)
            # ))

            date_picker_list.append(dcc.DatePickerSingle(
                id=prefix_id + id_,
                min_date_allowed=datetime.date.today() - datetime.timedelta(
                    days=365 * 3),
                max_date_allowed=datetime.date.today(),
                date=initial_date + datetime.timedelta(days=offset_),
                display_format='DD/MM/YY')
                # , style={'padding': 0, 'height' : 5, 'font-size' : '24px !important'},
            )

            # if i < len(id) - 1:
            #    date_picker_list.append(' to ')

        return html.Div(date_picker_list,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 0,
                               'marginTop': 0,
                               'marginLeft': 5,
                               'marginRight': 5})

    #
    # style = {'width': str(width) + 'px', 'display': 'inline-block', 'marginBottom': 0, 'marginTop': 0,
    #          'marginLeft': 5,
    #          'marginRight': 5}

    def date_picker_range(self, caption=None, id=None, prefix_id='',
                          initial_date=datetime.date.today(), width=None,
                          offset=[-7, -1]):
        if width is None: width = self._drop_down_width

        date_picker_list = []
        date_picker_list.append(caption + '      ')

        if prefix_id != '':
            prefix_id = prefix_id + '-'

        date_picker_list.append(dcc.DatePickerRange(
            id=prefix_id + id,
            min_date_allowed=datetime.date.today() - datetime.timedelta(
                days=120),
            max_date_allowed=datetime.date.today(),
            start_date=initial_date + timedelta(days=offset[0]),
            end_date_placeholder_text="Pick a date",
            display_format='DD/MM/YY'
        ))

        return html.Div(date_picker_list,
                        style={'width': str(width) + 'px',
                               'display': 'inline-block', 'marginBottom': 0,
                               'marginTop': 0,
                               'marginLeft': 5,
                               'marginRight': 5})

    def paragraph(self, text, id=None, prefix_id=''):
        if id is None:
            return html.P(text)
        else:
            if prefix_id != '':
                id = prefix_id + '-' + id

            return html.P(text, id=id)

    def markdown(self, text, id=None, prefix_id='', height=None, width=None,
                 wrap_in_div=True):
        if width is None: width = self._markdown_width

        if id is None:
            html_tags = dcc.Markdown(text)
        else:
            if prefix_id != '':
                id = prefix_id + '-' + id

            html_tags = dcc.Markdown(text, id=id)

        if height is None:
            html_style = {'width': str(width) + 'px', 'marginBottom': 0,
                          'marginTop': 0, 'marginLeft': 5,
                          'marginRight': 5}
        else:
            html_style = {'width': str(width) + 'px',
                          'height': str((height * len(id)) + 100) + 'px',
                          'marginBottom': 0, 'marginTop': 0, 'marginLeft': 5,
                          'marginRight': 5}

        if wrap_in_div:
            return html.Div(html_tags, style=html_style)

        return html_tags

    def dict_key_list(self, keys):

        # keys = di.keys()

        if isinstance(keys, list):
            return keys

        lst = []

        for k in keys:
            lst.append(k)

        return lst
