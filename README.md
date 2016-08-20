# chartpy

chartpy creates a simple easy to use API to plot in a number of great Python chart libraries like plotly (via cufflinks), bokeh and matplotlib,
with a unified interface. You simply need to change a single keyword to change which chart engine to use (see below), rather than having
to learn the low level details of each library. I've also created new stylesheets and formating to ensure that the default matplotlib
styling looks more modern using Open Sans font. Contributors for the project are very much welcome!

```
chart = Chart(df=df, chart_type='line', style=style)

# we now plot using multiple plotting libraries, with the same dataframe
chart.plot(engine='matplotlib')
chart.plot(engine='bokeh')
chart.plot(engine='plotly')
```

I had previously written the open source PyThalesians financial library. This new chartpy library has similar functionality to the chart
part of that library. However, I've totally rewritten the API to make it much cleaner and easier to use. It is also now a fully
standalone package, so it'll be easier to use for both non-financial and financial applications.

At present ChartPy supports several types of plots
* line (bokeh, plotly and matplotlib)
* scatter (bokeh, plotly and matplotlib)
* surface (plotly)
* map plots (plotly)
* looking to add more

Other points to note
* Please bear in mind at present chartpy is currently a highly experimental alpha project and isn't yet fully 
documented
* Uses Apache 2.0 licence

# To install Open Sans font

My chartpy stylesheet for matplotlib uses the free Open Sans font. For it to display properly you need to install Open Sans font
on your computer
* First download font from https://www.fontsquirrel.com/fonts/open-sans
* Windows: Install font by dragging to Windows/fonts folder
* Windows: Reset matplotlib font cache (delete file eg. c:/users/username/.matplotlib/fontList.py3k.cache
* On Mac OS X/Linux procedure for installing fonts is different

# Gallery

Doing plots in multiple libraries by simply changing a keyword, from the Jupyter notebook.

<img src="https://github.com/cuemacro/chartpy/blob/master/chartpy/examples/screenshot.png?raw=true" width="543"/>

Create subplots with minimal extra coding (see examples/subplot_examples.py)

<img src="https://github.com/cuemacro/chartpy/blob/master/chartpy/examples/subplot.png?raw=true" width="543"/>

Do surface plots (plotly only at present - see examples/surface_examples.py)

<img src="https://github.com/cuemacro/chartpy/blob/master/chartpy/examples/volsurface.png?raw=true" width="543"/>

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

* 20 Aug 2016 - Added Plotly default palette, surface examples
* 19 Aug 2016 - Added HTML examples for bokeh & plotly, subplotting for bokeh, plotly & matplotlib (with subplot_examples)
* 17 Aug 2016 - Uploaded first code

End of note
