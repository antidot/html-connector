import unittest
from pathlib import Path

from copro.html_connector.html_splitter_by_header import HtmlSplitterByHeader
from copro.html_connector.html_to_topics import HtmlToTopics, NeoTopic

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestHtmlToTopics(unittest.TestCase):

    maxDiff = None

    def test_broken_toc(self):
        # pylint: disable=expression-not-assigned,no-self-use
        class WorstSplitter:
            def split(self):
                return [{"title": "This won't work, we need the content and header_type keys"}]

        with self.assertRaises(RuntimeError) as rte:
            HtmlToTopics(WorstSplitter()).topics
        self.assertIn("Error when initializing topics", str(rte.exception))

        title = "Content can't be None"

        class WorseSplitter:
            def split(self):
                return [{"content": None, "header_type": "h1", "title": title}]

        with self.assertRaises(AssertionError) as rte:
            HtmlToTopics(WorseSplitter()).topics
        self.assertIn("Content related to '{}' should be a string".format(title), str(rte.exception))

        class BadSplitter:
            def split(self):
                return [
                    {
                        "content": "Valid content",
                        "children": ["We need a dict"],
                        "header_type": "h1",
                        "title": "Valid title",
                    }
                ]

        with self.assertRaises(TypeError) as rte:
            HtmlToTopics(BadSplitter()).topics
        self.assertIn("Expected a dict", str(rte.exception))

    def test_heading(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("heading.html"))
        toc_nodes = HtmlToTopics(splitter).topics
        expected = [
            NeoTopic(
                title="My First Heading",
                content="""

<p>My first paragraph.</p>

""",
            )
        ]
        self.assertEqual(toc_nodes, expected)

    def test_heading_three_level(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("heading_three_levels.html"))
        toc_nodes = HtmlToTopics(splitter).topics
        expected = [
            NeoTopic(
                title="Heading 1",
                content="\na\n",
                children=[
                    NeoTopic(
                        title="Heading 1-2",
                        content="\nb\n",
                        children=[NeoTopic(title="Heading 1-2-3", content="\nc\n")],
                    )
                ],
            )
        ]
        self.assertEqual(expected, toc_nodes)

    def test_headings(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("headings_simple.html"))
        toc_nodes = HtmlToTopics(splitter).topics
        expected = [
            NeoTopic(
                title="Heading 1",
                content="\na\n",
                children=[
                    NeoTopic(
                        title="Heading 1-2",
                        content="\nb\n",
                        children=[NeoTopic(title="Heading 1-2-3", content="\nc\n")],
                    )
                ],
            ),
            NeoTopic(title="Heading 1.2", content="\nd\n"),
            NeoTopic(title="Heading 1.3", content="\ne\n", children=[NeoTopic(title="Heading 1.3-2", content="\nf\n")]),
        ]
        for i, part in enumerate(toc_nodes):
            self.assertEqual(
                expected[i],
                part,
                "What we have:\n{}\n\n{}\nWhat we expect:\n{}\n\n".format(part, "-" * 80, expected[i]),
            )
