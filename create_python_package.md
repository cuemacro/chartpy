# Instructions for uploading a Python package

References
* https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
* https://packaging.python.org/tutorials/packaging-projects/

Install Twine if not already installed, which upload your project to PyPI
* pip install twine

Make sure we have properly prepared the package first ie. we need the following files properly prepared
* setup.py

If we are uploading a new version, make sure to change the version number in setup.py

Be careful to remove dist folder (otherwise later will try to re-upload old files)

Now create a distribution package
* python setup.py sdist bdist_wheel

For PyPI test environment upload (strongly recommend doing this first, in case you make a mistake)
* python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

For PyPI prod environment upload
* python -m twine upload dist/*