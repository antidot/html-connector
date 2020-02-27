import unittest
from pathlib import Path

from fluidtopics.connector import Metadata

from antidot.connector.generic.constants import ORIGIN_ID_MAX_SIZE
from antidot.connector.html.html_splitter_by_header import HtmlSplitterByHeader
from antidot.connector.html.html_to_fluid_api import get_html_from_path
from antidot.connector.html.html_to_topics import HtmlToTopics, NeoTopic

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestHtmlToFluidApi(unittest.TestCase):

    maxDiff = None

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

    def test_get_html_from_path(self):
        """Origin id is not gigantic even with a lot of metadata"""
        metadatas = []
        for i in range(1000):
            metadatas.append(Metadata.string("i", [-i, "long"]))
        _, name = get_html_from_path(Path(__file__), metadatas)
        print(name)
        self.assertLess(len(name), ORIGIN_ID_MAX_SIZE)
        _, other_name = get_html_from_path(Path(__file__), metadatas[:-1])
        self.assertNotEqual(name, other_name, "Different metadatas, same origin id !")
