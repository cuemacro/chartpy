from chartpy import Chart, Style

# choose run_example = 0 for everything
# run_example = 1 - plot volatility surface
run_example = 0

if run_example == 1 or run_example == 0:
    import pandas

    # get sample volatility surface for GBP/USD
    df = pandas.read_csv('volsurface.csv')

    # set the style of the plot
    style = Style(title="GBP/USD vol surface", source="chartpy", color='Blues')
    style.file_output = 'volsurface.png'

    # Chart object is initialised with the dataframe and our chart style
    chart = Chart(df=df, chart_type='surface', style=style)

    # chart.plot(engine='matplotlib')   TODO matplotlib implementation
    # chart.plot(engine='bokeh')        TODO bokeh surface implementation
    chart.plot(engine='plotly')