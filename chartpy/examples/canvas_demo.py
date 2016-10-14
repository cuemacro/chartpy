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

# choose run_example = 0 for everything
# run_example = 1 - create a plain and Keen.io based template for a chart webpage

run_example = 0

if run_example == 1 or run_example == 0:

    df = Quandl.get(["FRED/A191RL1Q225SBEA"], authtoken=quandl_api_key)
    df.columns = ["Real QoQ"]

    # Chart object is initialised with the dataframe and our chart style
    chart_bokeh = Chart(df=df, chart_type='line', engine='bokeh',
                        style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-2, width=500, height=300, silent_display=True))

    chart_plotly = Chart(df=df, chart_type='line', engine='plotly',
                         style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-2, width=500, height=300, silent_display=True))

    chart_matplotlib = Chart(df=df, chart_type='line', engine='matplotlib',
                             style=Style(title="US GDP", source="Quandl/Fred", scale_factor=-2, width=500, height=300, silent_display=True))

    text = "A demo of chartpy canvas!!"

    # using plain template
    canvas = Canvas([[text, chart_bokeh], [chart_plotly, df.tail(n=5)]])

    canvas.generate_canvas(silent_display=False, canvas_plotter='plain')

    # using the Keen template (needs static folder in the same place as final HTML file)
    canvas = Canvas([[chart_bokeh, chart_plotly], [chart_plotly, chart_matplotlib]])

    canvas.generate_canvas(silent_display=False, canvas_plotter='keen')