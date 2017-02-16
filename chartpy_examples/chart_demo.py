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

# support Quandl 3.x.x
try:
    import quandl as Quandl
except:
    # if import fails use Quandl 2.x.x
    import Quandl

from chartpy import Chart, Style

# get your own free Quandl API key from https://www.quandl.com/
try:
    from chartpy.chartcred import ChartCred

    cred = ChartCred()
    quandl_api_key = cred.quandl_api_key
except:
    quandl_api_key = "x"

# choose run_example = 0 for everything
# run_example = 1 - plot US GDP with multiple libraries
# run_example = 2 - plot US and UK unemployment demonstrating multiple line types
# run_example = 3 - correlations of a few different stocks in USA
run_example = 0

if run_example == 1 or run_example == 0:
    df = Quandl.get("FRED/GDP", authtoken=quandl_api_key)

    # we can use the charting tools in several ways
    chart = Chart()
    # chart.plot(df = df)

    # set the style of the plot
    style = Style(title="US GDP", source="Quandl/Fred")

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='line', style=style)

    # we now plot using multiple plotting libraries, with the same dataframe
    chart.plot(engine='matplotlib')
    chart.plot(engine='bokeh')
    chart.plot(engine='plotly')

if run_example == 2 or run_example == 0:
    # download US and Texas unemployment rate
    df = Quandl.get(["FRED/UNRATE", "FRED/TXUR"], authtoken=quandl_api_key, trim_start="2015-12-01")

    import pandas

    df.index = pandas.to_datetime(df.index, format='%Y-%m-%d')

    # first plot without any parameters (will use defaults) - note how we can it assign the dataframe to either Chart
    # or the plot method
    Chart(df).plot()
    Chart().plot(df)

    # we can also specify the engine within the Style object if we choose
    style = Style(title="US & Texas unemployment rate", chart_type=['bar', 'line'], engine='matplotlib')

    style.engine = 'bokeh'
    Chart(df, style=style).plot()

    # Bokeh wrapper doesn't yet support horizontal bars, but matplotlib and plotly/cufflink wrappers do
    style.engine = 'plotly'
    style.chart_type = 'barh'
    Chart(df, engine='plotly', style=style).plot()
    Chart(df, engine='matplotlib', style=style).plot()

if run_example == 3 or run_example == 0:
    df = Quandl.get(["WIKI/ABBV", "WIKI/TRIP", "WIKI/HPQ"], authtoken=quandl_api_key, trim_start="2016-06-01")

    # get only adjusted close field, calculate returns and create correlation matrix
    columns = [item for item in df.columns if " - Adj. Close" in item]
    df = df[columns]
    df.columns = [a.replace(' - Adj. Close', '') for a in df.columns]
    df = df / df.shift(1) - 1
    corr = df.corr() * 100

    print(corr)

    # set the style of the plot
    style = Style(title="Stock Correlations", source="Quandl/Fred", color='Blues')

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=corr, chart_type='heatmap', style=style)

    chart.plot(engine='matplotlib')
    # chart.plot(engine='bokeh')    # TODO
    chart.plot(engine='plotly')
