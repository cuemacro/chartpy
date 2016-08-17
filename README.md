# chartpy

chartpy creates a simple easy to use API to plot in a number of great Python chart libraries like Plotly, Bokeh and matplotlib,
with a unified interface. You simply need to change a single keyword to change which chart engine to use (see below), rather than having
to learn the low level details of each library. I've also created new stylesheets and formating to ensure that the default matplotlib
styling looks more modern.

```
chart = Chart(df=df, chart_type='line', style=style)

# we now plot using multiple plotting libraries, with the same dataframe
chart.plot(engine='matplotlib')
chart.plot(engine='bokeh')
chart.plot(engine='plotly')
```

I had previously written the open source PyThalesians library. This new chartpy library has similar functionality to the chart
part of that library. However, I've totally rewritten the API to make it much cleaner and easier to use.

* Please bear in mind at present chartpy is currently a highly experimental alpha project and isn't yet fully 
documented
* Uses Apache 2.0 licence

# Gallery

To appear here.

# Requirements

Major requirements
* Required: Python 3.4, 3.5
* Required: pandas, matplotlib, plotly, cufflinks, bokeh, numpy etc.

# Installation

You can install the library using the below. After installation:
* Make sure you edit the ChartConstants class for the correct Plotly API and Twitter API keys

```
pip install git+https://github.com/cuemacro/chartpy.git
```

# chartpy examples

In chartpy/examples you will find several demos

# Release Notes

* No formal releases yet

# Coding log

* 17 Aug 2016 - Uploaded first code

End of note
