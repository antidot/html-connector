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
        for file in ["headings.html", "malformed.html", "malformed2.html", "malformed3.html"]:
            splitter = BaseHtmlSplitter(path=Path(FIXTURE_DIR).joinpath(file))
            error_msg = "In {}".format(file)
            body = "body"
            if file == "malformed3.html":
                self.assertEqual(splitter.content.count(body), 1, error_msg)
            else:
                self.assertNotIn(body, splitter.content, error_msg)
            if "malformed" in file:
                background = 'class="page-background">'
                if file == "malformed3.html":
                    self.assertEqual(splitter.content.count(background), 1, error_msg)
                else:
                    self.assertNotIn(background, splitter.content, error_msg)
                for content in ["Introduction", "<h3>Heading 3</h3>", "a", "<h6>Heading 6</h6>", "b"]:
                    self.assertIn(content, splitter.content, error_msg)
