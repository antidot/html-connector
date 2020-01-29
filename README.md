# HTML connector

[![coverage report](https://scm.mrs.antidot.net/copro/html-connector/badges/master/coverage.svg)](https://scm.mrs.antidot.net/copro/html-connector/commits/master)



This connector permits to import HTML into FT by creating the table of
content automatically.

# Development

```
cd src/
python3 -m venv venv
source venv/bin/activate
# Use
pip3 install -e .
html2ft -h
# Test
pip3 install -e ".[test]"
python3 -m pytest . --cov=copro --cov-report html --verbose -vv
xdg-open htmlcov/index.html
```

# Usage
