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

import dash
import dash_html_components as html
import dash_core_components as dcc

from chartpy.dashboard import SketchComponents
from chartpy.chartconstants import ChartConstants

from dash.dependencies import Input, Output

from chartpy_examples.dashboard_examples.layoutchart import LayoutChart

from flask import Flask

server = Flask(__name__)
app = dash.Dash(name=__name__, server=server, url_base_pathname='/', serve_locally=True)
app.title = 'Cuemacro'

constants = ChartConstants()

app.config.update({
    'routes_pathname_prefix': '/',
    'requests_pathname_prefix': '/',
    })

app.config.suppress_callback_exceptions = True

sketch_components = SketchComponents(app=app, constants=constants)

# REPLACE THIS LINE WITH YOUR OWN QUANDL API KEY
quandl_api_key = constants.quandl_api_key

layout_chart = LayoutChart(app=app, constants=constants, quandl_api_key=quandl_api_key)

app.layout = layout_chart.construct_layout()

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server()