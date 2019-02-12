from setuptools import setup, find_packages

with open("longdesc.md", "r") as fh:
    long_description = fh.read()

setup(name='chartpy',
      version='0.1.0',
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
                        'twython',
                        'pytz',
                        'requests',
                        'numpy',
                        'plotly',
                        'cufflinks',
                        'bokeh',
                        'vispy'],
      zip_safe=False)
