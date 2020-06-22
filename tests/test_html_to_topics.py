import unittest
from pathlib import Path

from antidot.connector.html.html_splitter import HtmlSplitter
from antidot.connector.html.html_to_topics import HtmlToTopics, NeoTopic

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestHtmlToTopics(unittest.TestCase):

    maxDiff = None

    def test_empty_content(self):
        splitter = HtmlSplitter(content="")
        for render_cover_page in [True, False]:
            html2topics = HtmlToTopics(splitter, render_cover_page=render_cover_page)
            self.assertEqual(html2topics.topics, [])
            self.assertEqual(html2topics.resources, [])

    def test_broken_toc(self):
        # pylint: disable=expression-not-assigned,no-self-use
        class WorstSplitter:
            path = ""

            def split(self):
                return [{"title": "This won't work, we need the content and header_type keys"}]

        with self.assertRaises(RuntimeError) as rte:
            HtmlToTopics(WorstSplitter()).topics
        self.assertIn("Error when initializing topics", str(rte.exception))

        title = "Content can't be None"

        class WorseSplitter:
            path = ""

            def split(self):
                return [{"content": None, "header_type": "h1", "title": title, "id": None}]

        with self.assertRaises(AssertionError) as rte:
            HtmlToTopics(WorseSplitter()).topics
        self.assertIn("Content related to '{}' should be a string".format(title), str(rte.exception))

        class BadSplitter:
            path = ""

            def split(self):
                return [
                    {
                        "content": "Valid content",
                        "children": ["We need a dict"],
                        "header_type": "h1",
                        "title": "Valid title",
                        "id": None,
                    }
                ]

        with self.assertRaises(TypeError) as rte:
            HtmlToTopics(BadSplitter()).topics
        self.assertIn("Expected a dict", str(rte.exception))

    def test_heading(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("heading.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        expected = [
            NeoTopic(title="Cover Page", content="\n\nIntroduction\n\n"),
            NeoTopic(
                title="My First Heading",
                content="""

<p>My first paragraph.</p>

""",
            ),
        ]
        self.assertEqual(len(html2topics.resources), 0)
        self.assertEqual(html2topics.topics, expected)

    def test_heading_three_level(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("heading_three_levels.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        expected = [
            NeoTopic(title="Cover Page", content="\n\nIntroduction\n\n"),
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
        ]
        self.assertEqual(len(html2topics.resources), 0)
        self.assertEqual(expected, html2topics.topics)

    def test_headings(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("headings_simple.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        expected = [
            NeoTopic(title="Cover Page", content="z"),
            NeoTopic(
                title="Heading 1",
                content="\na\n",
                children=[
                    NeoTopic(
                        title="Heading 1-2", content="\nb\n", children=[NeoTopic(title="Heading 1-2-3", content="c")]
                    )
                ],
            ),
            NeoTopic(title="Heading 1.2", content="\nd\n"),
            NeoTopic(title="Heading 1.3", content="\ne\n", children=[NeoTopic(title="Heading 1.3-2", content="\nf\n")]),
        ]
        self.assertEqual(len(html2topics.resources), 0)
        for i, part in enumerate(html2topics.topics):
            self.assertEqual(
                expected[i],
                part,
                "What we have:\n{}\n\n{}\nWhat we expect:\n{}\n\n".format(part, "-" * 80, expected[i]),
            )

    def test_empty_title(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("empty_title.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        expected = [
            NeoTopic(
                title="Cover Page",
                origin_id=None,
                content="\n\nIntroduction\n\n    \nText that should be in the introduction.\n\n    ",
            ),
            NeoTopic(
                title="Installation",
                origin_id="_Ref2A4E1AB689A0D2EE52FF15610E2D8283",
                content="\n    a\n    \n    b\n\n    ",
            ),
            NeoTopic(title="Removal", origin_id="_Re2D8283", content="\n    c\n    \n    d\n  "),
        ]
        self.assertEqual(len(html2topics.resources), 0)
        self.assertEqual(html2topics.topics, expected)

    def test_anchor(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("anchor.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        expected = [
            NeoTopic(title="Cover Page", origin_id=None, content="\n\nIntroduction\n\n"),
            NeoTopic(title="Heading 1", origin_id="heading1", content='\n\nHeading 1\n\n<a href="heading2"></a>\n\n'),
            NeoTopic(
                title="Heading 2",
                origin_id="heading2",
                content="""
        Heading 2

        <a href="heading1"></a>

        <a href="https://google.com/#Heading2">Clique</a>

        """,
            ),
        ]
        self.assertEqual(len(html2topics.resources), 0)
        self.assertEqual(html2topics.topics, expected)

    def test_resource_creation(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("images.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        topics = html2topics.topics
        self.assertEqual(len(html2topics.resources), 6)
        self.assertEqual(len(topics), 1)
        self.assertEqual(len(topics[0].children), 12)
        self.assertEqual(topics[0].children[1].title, "The alt Attribute ")

    def test_cover_page(self):
        splitter = HtmlSplitter(
            content="""<!DOCTYPE html>
<html>
<body>
a
<h1>b</h1>
c
</body>
</html>
"""
        )
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        self.assertEqual(html2topics.resources, [])
        expected = [NeoTopic(title="Cover Page", content="a\n"), NeoTopic(title="b", content="c\n")]
        self.assertEqual(html2topics.topics, expected)
        html2topics = HtmlToTopics(splitter, render_cover_page=False)
        expected = expected[1:]
        self.assertEqual(html2topics.resources, [])
        self.assertEqual(html2topics.topics, expected)

    def test_empty_without_cover_page(self):
        splitter = HtmlSplitter(
            content="""<!DOCTYPE html>
<html>
<body>
a
b
c
</body>
</html>
"""
        )
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        self.assertEqual(html2topics.resources, [])
        expected_content = "a\nb\nc\n"
        expected = [NeoTopic(title="Cover Page", content=expected_content)]
        self.assertEqual(html2topics.topics, expected)
        html2topics = HtmlToTopics(splitter, render_cover_page=False)
        expected = [NeoTopic(title="Flat document", content=expected_content)]
        self.assertEqual(html2topics.resources, [])
        self.assertEqual(html2topics.topics, expected)

    def test_real_world_example(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("iphone5repare.html"))
        html2topics = HtmlToTopics(splitter, render_cover_page=True)
        self.assertEqual(len(html2topics.resources), 14)
        topics = html2topics.topics
        self.assertEqual(len(topics), 2)
        self.assertEqual(topics[1].title, "Comment remplacer la batterie de l'iPhone 5s")
        self.assertEqual(len(topics[1].children), 32)
        tool = topics[0].children[19]
        self.assertEqual(tool.title, "Outils")
        self.assertEqual(
            repr(tool),
            """<Topic>
    Title:
        Outils
    Content:
        <div><div class="sc-lkqHmb fRhhEx"></div></div>
    Children:
        []
</Topic>
""",
        )
