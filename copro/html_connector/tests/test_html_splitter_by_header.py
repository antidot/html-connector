import unittest
from pathlib import Path

from copro.html_connector.html_splitter_by_header import HtmlSplitterByHeader

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestHtmlSplitterByHeader(unittest.TestCase):

    maxDiff = None

    def test_simple_split(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("heading.html"))
        expected = [
            {
                "title": "My First Heading",
                "header_type": "h1",
                "content": """

<p>My first paragraph.</p>

""",
            }
        ]
        self.assertEqual(splitter.split(), expected)

    def test_simple_headings(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("standard_headings.html"))
        expected = [
            {
                "content": "\n\nIntroduction text 1a\n\n",
                "children": [
                    {"content": "\n\nParagraph text 1a-2a\n\n", "header_type": "h2", "title": "Heading 1a-2a"},
                    {"content": "\n\nParagraph text 1a-2b\n\n", "header_type": "h2", "title": "Heading 1a-2b"},
                ],
                "header_type": "h1",
                "title": "Heading 1a",
            },
            {
                "content": "\n\nIntroduction text 1b\n\n",
                "children": [
                    {"content": "\n\nParagraph text 1b-2a\n\n", "header_type": "h2", "title": "Heading 1b-2a"},
                    {"content": "\n\nParagraph text 1b-2b\n\n", "header_type": "h2", "title": "Heading 1b-2b"},
                ],
                "header_type": "h1",
                "title": "Heading 1b",
            },
        ]
        self.assertEqual(splitter.split(), expected)

    def test_simple_split_with_text(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("headings_simple.html"))
        expected = [
            {
                "content": "\na\n",
                "children": [
                    {
                        "content": "\nb\n",
                        "children": [{"content": "\nc\n", "header_type": "h3", "title": "Heading 1-2-3"}],
                        "header_type": "h2",
                        "title": "Heading 1-2",
                    }
                ],
                "header_type": "h1",
                "title": "Heading 1",
            },
            {"content": "\nd\n", "header_type": "h1", "title": "Heading 1.2"},
            {
                "content": "\ne\n",
                "children": [{"content": "\nf\n", "header_type": "h2", "title": "Heading 1.3-2"}],
                "header_type": "h1",
                "title": "Heading 1.3",
            },
        ]
        self.assertEqual(splitter.split(), expected)

    def test_table_split(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("tables.html"))
        expected = [
            {
                "content": """

<p>HTML tables start with a table tag.</p>
<p>Table rows start with a tr tag.</p>
<p>Table data start with a td tag.</p>

<hr>
""",
                "header_type": "h2",
                "title": "HTML Tables",
            },
            {
                "content": """

<table>
  <tr>
    <td>100</td>
  </tr>
</table>

<hr>
""",
                "header_type": "h2",
                "title": "1 Column:",
            },
            {
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
                "header_type": "h2",
                "title": "1 Row and 3 Columns:",
            },
            {
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
                "header_type": "h2",
                "title": "3 Rows and 3 Columns:",
            },
        ]
        self.assertEqual(splitter.split(), expected)
