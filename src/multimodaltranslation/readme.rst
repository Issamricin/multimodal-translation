In order to add the coverage report to readthedocs:
===================================================

First, pytest --cov=src --cov-report=html
and make sure you install: pip install pytest-cov coverage

This will create the coverage html page. You need to move the whole folder into the _static folder in the readthedocs folder.

then you can create report coverage page: 

# Coverage Report
# ---------------
# 
# .. raw:: html
# 
#     <iframe src="../../_static/coverage_html_report/index.html" width="100%" height="800"></iframe>
# 
