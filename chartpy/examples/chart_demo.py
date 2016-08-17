# support Quandl 3.x.x
try:
    import quandl as Quandl
except:
    # if import fails use Quandl 2.x.x
    import Quandl

from chartpy import Chart, Style

# get your own free bQuandl API key from https://www.quandl.com/
quandl_api_key = "xxx"

# choose run_example = 0 for everything
# run_example = 1 - plot US GDP with multiple libraries
# run_example = 2 - plot US and UK unemployment demonstrating multiple line types
run_example = 0

if run_example == 1 or run_example == 0:
    df = Quandl.get("FRED/GDP", authtoken=quandl_api_key)

    # we can use the charting tools in several ways
    chart = Chart()
    chart.plot(df = df)

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

    # first plot without any parameters (will use defaults) - note how we can it assign the dataframe to either Chart
    # or the plot method
    Chart(df).plot()
    Chart().plot(df)

    # we can also specify the engine within the Style object if we choose
    style = Style(title="US & Texas unemployment rate", chart_type=['bar', 'line'], engine='matplotlib')

    Chart(df, style=style).plot()
