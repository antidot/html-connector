import unittest
from pathlib import Path

from antidot.connector.html.html_splitter import BaseHtmlSplitter

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestBaseHtmlSplitter(unittest.TestCase):

    maxDiff = None

    def test_normalize(self):
        html = """

<p>      My first paragraph.          </p>

"""
        expected = """<p>
 My first paragraph.
</p>
"""
        self.assertEqual(BaseHtmlSplitter.normalize_html(html), expected)
        html = """

Introduction text 1a

<h2>Heading 1a-2a</h2>

Paragraph text 1a-2a

<h2>Heading 1a-2b</h2>

Paragraph text 1a-2b

"""
        expected = """Introduction text 1a
<h2>
 Heading 1a-2a
</h2>
Paragraph text 1a-2a
<h2>
 Heading 1a-2b
</h2>
Paragraph text 1a-2b
"""
        self.assertEqual(BaseHtmlSplitter.normalize_html(html), expected)

    def test_cut_body(self):
        splitter = BaseHtmlSplitter(path=Path(FIXTURE_DIR).joinpath("headings.html"))
        self.assertNotIn("body", splitter.content)
