from antidot.connector.html.html_splitter import BaseHtmlSplitter

EXPECTED_TABLES = [
    {"title": "Cover Page", "content": "\n\nExample taken on w3c website.\n\n"},
    {
        "title": "HTML Tables",
        "content": """

<p>HTML tables start with a table tag.</p>
<p>Table rows start with a tr tag.</p>
<p>Table data start with a td tag.</p>

<hr>
""",
    },
    {
        "title": "1 Column:",
        "content": """

<table>
  <tr>
    <td>100</td>
  </tr>
</table>

<hr>
""",
    },
    {
        "title": "1 Row and 3 Columns:",
        "content": """
<table>
  <tr>
    <td>100</td>
    <td>200</td>
    <td>300</td>
  </tr>
</table>

<hr>
""",
    },
    {
        "title": "3 Rows and 3 Columns:",
        "content": """
<table>
  <tr>
    <td>100</td>
    <td>200</td>
    <td>300</td>
  </tr>
  <tr>
    <td>400</td>
    <td>500</td>
    <td>600</td>
  </tr>
  <tr>
    <td>700</td>
    <td>800</td>
    <td>900</td>
  </tr>
</table>

<hr>

""",
    },
]


def get_table_with_headers():
    table_with_headers = []
    for dict_ in EXPECTED_TABLES:
        temp = {}
        for key, value in dict_.items():
            temp[key] = value
        temp["header_type"] = "h2"
        table_with_headers.append(temp)
    return table_with_headers


EXPECTED_TABLES_HEADER = get_table_with_headers()


def normalize_html(html):
    return BaseHtmlSplitter.normalize_html(html)
