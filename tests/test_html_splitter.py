import unittest
from pathlib import Path

from antidot.connector.html.html_splitter import HtmlSplitter

from .common import EXPECTED_TABLES

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestHtmlSplitter(unittest.TestCase):

    maxDiff = None

    def test_init(self):
        HtmlSplitter('<a href="http://example.com/?foo=val1&bar=val2">A link</a>')
        with self.assertRaises(ValueError) as e:
            HtmlSplitter("<div>/div>", "/tmp/path/to_file.html")
        self.assertEqual(str(e.exception), "Choose only one between <content> and <path>.")
        with self.assertRaises(ValueError) as e:
            HtmlSplitter()
        self.assertEqual(str(e.exception), "Choose at least one between <content> and <path>.")
        with self.assertRaises(FileNotFoundError) as e:
            HtmlSplitter(path="this/path/does/not/exists.html")
        self.assertEqual(str(e.exception), "[Errno 2] No such file or directory: 'this/path/does/not/exists.html'")
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("example.html"))
        self.assertIsNotNone(splitter.content)
        splitter = HtmlSplitter(content="")
        self.assertEqual(splitter.split("h1"), [])

    def test_heading_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("heading.html"))
        expected = [
            {
                "title": "My First Heading",
                "content": """

<p>My first paragraph.</p>

""",
            }
        ]
        self.assertEqual(splitter.split("h1"), expected)

    def test_empty_title(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("empty_title.html"))
        expected = [
            {"title": "Installation", "content": "\n    a\n    \n    b\n\n    "},
            {"title": "Removal", "content": "\n    c\n    \n    d\n  "},
        ]
        self.assertEqual(splitter.split("h1"), expected)

    def test_simple_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("standard_headings.html"))
        expected = [
            {
                "content": """

Introduction text 1a

<h2>Heading 1a-2a</h2>

Paragraph text 1a-2a

<h2>Heading 1a-2b</h2>

Paragraph text 1a-2b

""",
                "title": "Heading 1a",
            },
            {
                "content": """

Introduction text 1b

<h2>Heading 1b-2a</h2>

Paragraph text 1b-2a

<h2>Heading 1b-2b</h2>

Paragraph text 1b-2b

""",
                "title": "Heading 1b",
            },
        ]
        self.assertEqual(splitter.split("h1"), expected)
        expected = [
            {"content": "\n\nParagraph text 1a-2a\n\n", "title": "Heading 1a-2a"},
            {
                "content": "\n"
                "\n"
                "Paragraph text 1a-2b\n"
                "\n"
                "<h1>Heading 1b</h1>\n"
                "\n"
                "Introduction text 1b\n"
                "\n",
                "title": "Heading 1a-2b",
            },
            {"content": "\n\nParagraph text 1b-2a\n\n", "title": "Heading 1b-2a"},
            {"content": "\n\nParagraph text 1b-2b\n\n", "title": "Heading 1b-2b"},
        ]
        self.assertEqual(splitter.split("h2"), expected)

    def test_multiple_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("headings.html"))
        expected = [
            {
                "title": "Heading 1",
                "content": """
<h2>Heading 1-2</h2>
<h3>Heading 1-2-3</h3>
<h4>Heading 1-2-3-4</h4>
<h5>Heading 1-2-3-4-5</h5>
<h6>Heading 1-2-3-4-5-6</h6>

Actual h6 text

<h2>Heading 1-2.2</h2>
<h3>Heading 1-2.2-3</h3>

""",
            },
            {
                "title": "Heading 1.2",
                "content": """
<h2>Heading 1.2-2</h2>

""",
            },
            {
                "title": "Heading 1.3",
                "content": """
<h2>Heading 1.3-2</h2>

""",
            },
        ]
        self.assertEqual(splitter.split("h1"), expected)
        h2_expecteds = [
            [
                {
                    "title": "Heading 1-2",
                    "content": """
<h3>Heading 1-2-3</h3>
<h4>Heading 1-2-3-4</h4>
<h5>Heading 1-2-3-4-5</h5>
<h6>Heading 1-2-3-4-5-6</h6>

Actual h6 text

""",
                },
                {
                    "title": "Heading 1-2.2",
                    "content": """
<h3>Heading 1-2.2-3</h3>

""",
                },
            ],
            [{"title": "Heading 1.2-2", "content": "\n\n"}],
            [{"title": "Heading 1.3-2", "content": "\n\n"}],
        ]
        for test_value, h2_expected in zip(expected, h2_expecteds):
            splitter = HtmlSplitter(test_value["content"])
            self.assertEqual(splitter.split("h2"), h2_expected)

    def test_tables(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("tables.html"))
        self.assertEqual(splitter.split("h1"), [])
        self.assertEqual(splitter.split("h2"), EXPECTED_TABLES)
        self.assertEqual(splitter.split("h7"), [])

    def test_real_world_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("iphone5repare.html"))
        self.assertEqual(len(splitter.split("h1")), 1)
        self.assertEqual(len(splitter.split("h2")), 31)
        self.assertEqual(len(splitter.split("h3")), 40)
