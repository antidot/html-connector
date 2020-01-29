# HTML connector

[![coverage report](https://scm.mrs.antidot.net/copro/html-connector/badges/master/coverage.svg)](https://scm.mrs.antidot.net/copro/html-connector/commits/master)

This connector permits to import HTML into FT by creating the table of
content automatically.

# Installing

```bash
pip3 install copro-html-connector -i https://pypi.mrs.antidot.net/antidot/stable/
```


# Development

```bash
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

## Default behavior

### Sending directly to FT

If you want to send your data directly to FluidTopics:

```python
from copro.html_connector import  html_to_published_fluid_api

html_to_published_fluid_api(html_path, url, login, password)
```

### Getting the intermediary publications objects

If you want to get the publications from your html file:
```python
from copro.html_connector import html_to_fluid_api

publication = html_to_fluid_api(html_path, title)
```

## Optional arguments

### FTML splitting algorithm

You can use the FTML splitting algorithm. In this case add the use_ftml parameter:

```python
from copro.html_connector import  html_to_published_fluid_api, html_to_fluid_api

html_to_published_fluid_api(html_path, url, login, password, use_ftml=True)
publication = html_to_fluid_api(html_path, title, use_ftml=True)
```

### Adding metadata

You can also add metadata to the publication. In order to do that give a
list of metadata with the metadatas parameter:

```python
from fluidtopics.connector import Metadata
from copro.html_connector import html_to_fluid_api, html_to_published_fluid_api

from datetime import datetime

use_ftml = True
metadatas = [
    Metadata.string("splitting_algorithm", ["ftml" if use_ftml else "default"]),
    Metadata.last_edition(datetime.now().strftime("%Y-%m-%d")),
]
html_to_published_fluid_api(html_path, url, login, password, use_ftml=use_ftml, metadatas=metadatas)
publication = html_to_fluid_api(html_path, title, use_ftml=True, metadatas=metadatas)
```
