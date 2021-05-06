__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2021 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

import pandas as pd
import datetime
import math

import quandl

from chartpy import Chart, Style
from chartpy.dashboard import LayoutCanvas, CallbackManager

class LayoutChart(LayoutCanvas):

    def __init__(self, app=None, constants=None, quandl_api_key=None):
        super().__init__(app=app, constants=constants)

        self._callback_manager = CallbackManager(constants=constants)

        self._drop_down_width = 120
        self._quandl_api_key = quandl_api_key

        quandl.ApiConfig.api_key = self._quandl_api_key

        self.attach_callbacks()

    def attach_callbacks(self):

        output = self._callback_manager.output_callback(self.page_id(),
                                                        ['spot-fig',
                                                         'vol-fig',
                                                         'msg-status'])
        input = self._callback_manager.input_callback(self.page_id(), 'calculate-button')
        state = self._callback_manager.state_callback(self.page_id(), ['ticker-val'])

        self._app.callback(*output, *input, *state)(self.calculate_button)

    def calculate_button(self, *args):

        n_clicks, ticker = args

        if ticker == '': return {}, "Here is an example of using chartpy with dash"

        try:
            df = pd.DataFrame(quandl.get(ticker))

            df_vol = (df / df.shift(1)).rolling(window=20).std()* math.sqrt(252) * 100.0

            spot_fig = Chart(engine="plotly").plot(df,
                            style=Style(title='Spot', plotly_plot_mode='dash', width=980, height=480, scale_factor=-1))

            vol_fig = Chart(engine="plotly").plot(df_vol,
                                                     style=Style(title='Realized Vol 1M', plotly_plot_mode='dash', width=980,
                                                                 height=480, scale_factor=-1))
            msg = "Plotted " + ticker + " at " + datetime.datetime.utcnow().strftime("%b %d %Y %H:%M:%S")

            return spot_fig, vol_fig, msg
        except Exception as e:
            print(str(e))
            pass

        return {}, "Failed to download"

    def page_name(self):
        return "Example"

    def page_id(self):
        return "example"

    def construct_layout(self):

        return self._sc.extra_width_row_cell(
            [
                self._sc.header_bar(
                    self.page_name(), img='logo.png', id=['msg-status', 'help-status'], prefix_id=self.page_id(),
                    description=['Here is an example of using chartpy with dash',
                                 "Redrawn at " + datetime.datetime.utcnow().strftime("%b %d %Y %H:%M:%S")]),

                self._sc.horizontal_bar(),

                self._sc.row_cell([self._sc.inputbox(caption='Quandl Ticker', id='ticker-val',
                                                     prefix_id=self.page_id(),
                                                     start_values='FRED/DEXUSEU',
                                                     width=980)]),

                self._sc.horizontal_bar(),

                self._sc.button(caption='Calculate', id='calculate-button', prefix_id=self.page_id()),

                self._sc.horizontal_bar(),

                self._sc.plot("Quandl Plot", id=['spot-fig', 'vol-fig'], prefix_id=self.page_id(), height=500),
            ]
        )

