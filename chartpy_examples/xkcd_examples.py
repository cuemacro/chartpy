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
# run_example = 1 - xkcd example
run_example = 0

if run_example == 1 or run_example == 0:
    df = Quandl.get(["FRED/A191RL1Q225SBEA"], authtoken=quandl_api_key)
    df.columns = ["Real QoQ"]

    # set the style of the plot
    style = Style(title="US GDP", source="Quandl/Fred", xkcd=True)

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='line', style=style, engine='matplotlib')

    chart.plot()