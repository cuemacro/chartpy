# support Quandl 3.x.x
try:
    import quandl as Quandl
except:
    # if import fails use Quandl 2.x.x
    import Quandl

from chartpy import Chart, Style

# get your own free bQuandl API key from https://www.quandl.com/
try:
    from chartpy.chartcred import ChartCred

    cred = ChartCred()
    quandl_api_key = cred.quandl_api_key
except:
    quandl_api_key = "x"

# choose run_example = 0 for everything
# run_example = 1 - plot US GDP QoQ (real) and nominal with Plotly/Bokeh/Matplotlib with subplots for each line
# run_example = 2 - plot US GDP QoQ (real + nominal) in two double plots (passing an array of dataframes)
run_example = 0

if run_example == 1 or run_example == 0:
    df = Quandl.get(["FRED/A191RL1Q225SBEA", "FRED/A191RP1Q027SBEA"], authtoken=quandl_api_key)
    df.columns = ["Real QoQ", "Nominal QoQ"]

    # set the style of the plot
    style = Style(title="US GDP", source="Quandl/Fred", subplots=True)

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='line', style=style)

    chart.plot(engine='matplotlib')
    chart.plot(engine='bokeh')
    chart.plot(engine='plotly')

if run_example == 2 or run_example == 0:
    df = Quandl.get(["FRED/A191RL1Q225SBEA", "FRED/A191RP1Q027SBEA"], authtoken=quandl_api_key)
    df.columns = ["Real QoQ", "Nominal QoQ"]

    df = [df, df]

    # set the style of the plot
    style = Style(title="US GDP double plot", source="Quandl/Fred", subplots=True)

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='line', style=style)

    chart.plot(engine='bokeh')
    chart.plot(engine='matplotlib')
    chart.plot(engine='plotly') # TODO fix legends though

