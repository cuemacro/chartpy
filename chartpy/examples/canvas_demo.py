# support Quandl 3.x.x
try:
    import quandl as Quandl
except:
    # if import fails use Quandl 2.x.x
    import Quandl

from chartpy import Chart, Style, Canvas

# get your own free bQuandl API key from https://www.quandl.com/
try:
    from chartpy.chartcred import ChartCred

    cred = ChartCred()
    quandl_api_key = cred.quandl_api_key
except:
    quandl_api_key = "x"

if True:

    df = Quandl.get(["FRED/A191RL1Q225SBEA"], authtoken=quandl_api_key)
    df.columns = ["Real QoQ"]

    # Chart object is initialised with the dataframe and our chart style
    chart_bokeh = Chart(df=df, chart_type='line', engine='bokeh',
                        style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-1, width=500, height=300, silent_display=True))

    chart_plotly = Chart(df=df, chart_type='line', engine='plotly',
                         style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-1, width=500, height=300, silent_display=True))

    chart_matplotlib = Chart(df=df, chart_type='line', engine='matplotlib',
                             style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-1, width=500, height=300, silent_display=True))

    text = "A demo of chartpy canvas!!"

    canvas = Canvas([[text, chart_bokeh], [chart_plotly, df.tail(n=5)]])

    canvas.generate_canvas(silent_display=False, canvas_plotter='plain')