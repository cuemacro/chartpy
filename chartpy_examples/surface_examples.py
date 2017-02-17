__author__ = 'saeedamen'  # Saeed Amen

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

from chartpy import Chart, Style

# choose run_example = 0 for everything
# run_example = 1 - plot volatility surface
run_example = 0

if run_example == 1 or run_example == 0:
    import pandas

    # get sample volatility surface for GBP/USD (and make sure columns are in reasonable order)
    df = pandas.read_csv('volsurface.csv', index_col='Exp')
    df = df[['10D Put GBP', '25D Put GBP', 'ATM', '25D Call GBP', '10D Call GBP']]

    # set the style of the plot
    style = Style(title="GBP/USD vol surface", source="chartpy", color='Blues')
    style.file_output = 'volsurface.png'

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='surface', style=style)

    chart.plot(engine='matplotlib')
    # chart.plot(engine='bokeh')        # TODO bokeh surface implementation
    chart.plot(engine='plotly')