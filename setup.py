from setuptools import setup, find_packages

long_description = """chartpy creates a simple easy to use API to plot in a number of great Python chart libraries like plotly (via cufflinks),
bokeh and matplotlib, with a unified interface. You simply need to change a single keyword to change which chart engine
to use (see below), rather than having to learn the low level details of each library. I've also created new stylesheets
and formatting to ensure that the default matplotlib styling looks more modern using Open Sans font. The library
also works well with Dash, plotly's web server library built on top of Flask."""

setup(name='chartpy',
      version='0.1.4',
      description='chartpy creates a simple easy to use API to plot in a number of great Python chart libraries',
      author='Saeed Amen',
      author_email='saeed@cuemacro.com',
      long_description=long_description,
      license='Apache 2.0',
      keywords=['pandas', 'chart', 'plot', 'plotly'],
      url='https://github.com/cuemacro/chartpy',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['pandas',
                        'matplotlib',
                        'pdfkit',
                        'twython',
                        'pytz',
                        'requests',
                        'numpy',
                        'plotly',
                        'cufflinks',
                        'bokeh',
                        'vispy'],
      zip_safe=False)
