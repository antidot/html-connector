# HTML connector

This connector permits to import HTML into your FluidTopics instance from
your local computer or anything that can run Python3. It creates the table
of content automatically from the content of your HTML file. The result should
be available in FluidTopics as soon as the content processing end.

# Example

You have an HTML file `lorem.html`:

![HTML to import](doc/static/lorem_html.png "HTML to import")


And a FluidTopics tenant up and running at "my.fluidtopics.tenant.url".
You need to have a working python environement locally and to have
installed the html connector (see "Installing").

```bash
#  Send "lorem.html" to the FT instance
html2ft lorem.html --url my.fluidtopics.tenant.url --login my@ddress.com --password mypassword
```

You can see your import in the content processing:

![Content processing](doc/static/lorem_content_processing.png "Content processing")

And your document is uploaded in FluidTopics with a generated table of content:

![lorem in Fluid topics](doc/static/lorem_ft.png "Lorem in Fluid Topics")

# Installing

## Client

You need to have a working python3 environment on your machine.

For example, if your on MacOs it means installing pip3 with `brew install pip3`.

```bash
pip3 install fluidtopics -U # Necessary because the latest fluidtopics is not on pypi.mrs
pip3 install antidot-html-connector -i https://pypi.mrs.antidot.net/antidot/stable/
```

## FT Server

You need to add the external source with ID = `HTMLConnector`. Please
make it known here (https://jira.antidot.net/browse/FT-4795)
if you want to not have to do that.

# Usage

## Using as a binary

The `html2ft` binary will publish the HTML document in your FluidTopics
instance and create its table of content automatically.

```
html2ft path/to/file.html --url my.fluidtopics.tenant.url --login my@ddress.com
```

You can add the `--verbose` or `--password myStr0ngP@ssword` options.

## Using as a library

### Sending directly to FT

If you want to send your data directly to FluidTopics:

```python
from antidot.connector.html import publish_html

publish_html(html_path, url, login, password)
```

You can also use a Client object from the fluidtopics package:

```python
from fluidtopics.connector import RemoteClient
from antidot.connector.html import publish_html_with_client

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

### Optional FTML splitting algorithm

If you can and want to use the FTML you also need to install the FTML connector:

```bash
pip3 install antidot-fluidtopics-ftml-connector -i https://pypi.mrs.antidot.net/antidot/stable/
```

You can then use the binary with the `--use-ftml` option.

If the FTML connector is installed you can then add the `use_ftml` parameter:

```python
from antidot.connector.html import publish_html, publish_html_with_client, html_to_fluid_api
from fluidtopics.connector import RemoteClient

publish_html(html_path, url, login, password, use_ftml=True)
publish_html_with_client(html_path, RemoteClient(url, login, password, source_id), use_ftml=True)
publication = html_to_fluid_api(html_path, title, use_ftml=True)
```

# Development

[![coverage report](https://scm.mrs.antidot.net/copro/html-connector/badges/master/coverage.svg)](https://scm.mrs.antidot.net/copro/html-connector/commits/master)

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
