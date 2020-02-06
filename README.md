# HTML connector

[![coverage report](https://scm.mrs.antidot.net/copro/html-connector/badges/master/coverage.svg)](https://scm.mrs.antidot.net/copro/html-connector/commits/master)

This connector permits to import HTML into FT by creating the table of
content automatically.

# Installing

```bash
pip3 install antidot-html-connector -i https://pypi.mrs.antidot.net/antidot/stable/
```

# Optional split algorithm

If you can and want to use the FTML you also need to install the FTML connector:

```bash
pip3 install antidot-fluidtopics-ftml-connector -i https://pypi.mrs.antidot.net/antidot/stable/
```

# Development

```bash
python3 -m venv venv
source venv/bin/activate
# Use
pip3 install -e .
html2ft -h
# Test
pip3 install -e ".[test]"
python3 -m pytest . --cov=antidot --cov-report html --verbose -vv
xdg-open htmlcov/index.html
```

# Usage

## Using as a binary

Install the python package, then you can use the `html2ft` binary.

```
html2ft path/to/file.html --url my.fluidtopics.tenant.url --login my@ddress.com
```

You can add the `--verbose` or `--password myStr0ngP@ssword` options.

If you want to use the FTML connector for splitting your HTML and if
it's installed, you can use the `--use-ftml` option.

## Using as a library

### Sending directly to FT

If you want to send your data directly to FluidTopics:

```python
from antidot.connector.html import publish_html, publish_html_with_client

publish_html(html_path, url, login, password)

# Or use a Client from the fluidtopics package.
from fluidtopics.connector import RemoteClient

client = RemoteClient(url, login, password, source_id)
publish_html_with_client(html_path, client=client)
```

### Getting the intermediary publications objects

If you want to get the publications from your html file:
```python
from antidot.connector.html import html_to_fluid_api

publication = html_to_fluid_api(html_path, title)
```

## Optional arguments

### FTML splitting algorithm

You can use the FTML splitting algorithm. You will need to install the
FTML connector first. Once it's done you can then add the `use_ftml` parameter:

```python
from antidot.connector.html import publish_html, publish_html_with_client, html_to_fluid_api
from fluidtopics.connector import RemoteClient

publish_html(html_path, url, login, password, use_ftml=True)
publish_html_with_client(html_path, RemoteClient(url, login, password, source_id), use_ftml=True)
publication = html_to_fluid_api(html_path, title, use_ftml=True)
```

### Adding metadata

You can also add metadata to the publication. In order to do that give a
list of metadata with the metadatas parameter:

```python
from datetime import datetime

from fluidtopics.connector import Metadata, RemoteClient
from antidot.connector.html import html_to_fluid_api, publish_html, publish_html_with_client

use_ftml = True
metadatas = [
    Metadata.string("splitting_algorithm", ["ftml" if use_ftml else "default"]),
    Metadata.last_edition(datetime.now().strftime("%Y-%m-%d")),
]
publish_html(html_path, url, login, password, use_ftml=use_ftml, metadatas=metadatas)
publish_html_with_client(html_path, RemoteClient(url, login, password, source_id), metadatas, use_ftml)
publication = html_to_fluid_api(html_path, title, use_ftml=True, metadatas=metadatas)
```
