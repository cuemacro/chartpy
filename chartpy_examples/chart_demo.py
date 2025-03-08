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

import pandas as pd

from chartpy import Chart, Style

df_fx = pd.read_csv("https://raw.githubusercontent.com/cuemacro/teaching/refs/heads/master/pythoncourse/data/daily_fx_spot_data.csv", index_col=0)
df_fx.index = pd.to_datetime(df_fx.index, format='%Y-%m-%d')

run_example = 3

if run_example == 1 or run_example == 0:

    # We can use the charting tools in several ways

    # Set the style of the plot
    style = Style(title="EURUSD", source="FRED", auto_scale=True, chart_type="line")

    chart = Chart(engine="plotly")

    # Chart object is initialised with the dataframe and our chart style
    chart.plot(df=df_fx["EURUSD.close"], style=style)

    style.mode = "markers"
    style.chart_type = "dot"
    chart.plot(df=df_fx["EURUSD.close"], style=style)

    # We now plot using multiple plotting libraries, with the same dataframe
    chart.plot(engine='matplotlib', df=df_fx["EURUSD.close"], style=style)

    style.subplots = True
    style.subplot_titles = ["EURUSD", "GBPUSD"]
    chart.plot(df=[df_fx["EURUSD.close"], df_fx["GBPUSD.close"]], style=style)

if run_example == 2 or run_example == 0:

    # first plot without any parameters (will use defaults) - note how we can it assign the dataframe to either Chart
    # or the plot method

    df_month_end = df_fx[["EURUSD.close", "GBPUSD.close"]].resample('M').last()
    df_month_end = (df_month_end / df_month_end.shift(1) - 1.0) * 100

    df_month_end  = df_month_end.tail(12)

    # We can also specify the engine within the Style object if we choose
    style = Style(title="FX charts", chart_type=['bar', 'line'])

    Chart(df=df_month_end, engine='plotly', style=style).plot()

    style.chart_type = 'barh'
    Chart(df=df_month_end, engine='plotly', style=style).plot()
    Chart(df=df_month_end, engine='matplotlib', style=style).plot()

if run_example == 3 or run_example == 0:
    df = df_fx[["EURUSD.close", "GBPUSD.close"]].resample('M').last()

    # get only adjusted close field, calculate returns and create correlation matrix
    df = df / df.shift(1) - 1
    corr = df.corr() * 100

    print(corr)

    # Set the style of the plot
    style = Style(title="FX Correlations", source="FRED", color='Blues')

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=corr, chart_type='heatmap', style=style)

    chart.plot(engine='matplotlib')
    chart.plot(engine='plotly')
