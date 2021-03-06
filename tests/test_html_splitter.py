import unittest
from pathlib import Path

from antidot.connector.html.html_splitter import HtmlSplitter

from .common import EXPECTED_TABLES_HEADER

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
        self.assertEqual(splitter.split(), [])

    def test_simple_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("heading.html"))
        expected = [
            {"content": "\n\nIntroduction\n\n", "header_type": "h1", "title": "Cover Page", "id": None},
            {
                "title": "My First Heading",
                "header_type": "h1",
                "content": "\n\n<p>My first paragraph.</p>\n\n",
                "id": None,
            },
        ]
        self.assertEqual(splitter.split(), expected)

    def test_empty_title(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("empty_title.html"))
        expected = [
            {
                "content": "\n\nIntroduction\n\n    \n\nText that should be in the introduction.\n\n    ",
                "header_type": "h1",
                "title": "Cover Page",
                "id": None,
            },
            {
                "title": "Installation",
                "content": "\n    a\n    \n    b\n\n    ",
                "header_type": "h1",
                "id": "_Ref2A4E1AB689A0D2EE52FF15610E2D8283",
            },
            {"title": "Removal", "content": "\n    c\n    \n    d\n  ", "header_type": "h1", "id": "_Re2D8283"},
        ]
        self.assertEqual(splitter.split(), expected)

    def test_simple_headings(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("standard_headings.html"))
        expected = [
            {"content": "\n\nIntroduction text document.\n\n", "title": "Cover Page", "header_type": "h1", "id": None},
            {
                "content": "\n\nIntroduction text 1a\n\n",
                "children": [
                    {
                        "content": "\n\nParagraph text 1a-2a\n\n",
                        "header_type": "h2",
                        "title": "Heading 1a-2a",
                        "id": None,
                    },
                    {
                        "content": "\n\nParagraph text 1a-2b\n\n",
                        "header_type": "h2",
                        "title": "Heading 1a-2b",
                        "id": None,
                    },
                ],
                "header_type": "h1",
                "title": "Heading 1a",
                "id": None,
            },
            {
                "content": "\n\nIntroduction text 1b\n\n",
                "children": [
                    {
                        "content": "\n\nParagraph text 1b-2a\n\n",
                        "header_type": "h2",
                        "title": "Heading 1b-2a",
                        "id": None,
                    },
                    {
                        "content": "\n\nParagraph text 1b-2b\n\n",
                        "header_type": "h2",
                        "title": "Heading 1b-2b",
                        "id": None,
                    },
                ],
                "header_type": "h1",
                "title": "Heading 1b",
                "id": None,
            },
        ]
        self.assertEqual(splitter.split(), expected)

    def test_simple_split_with_text(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("headings_simple.html"))
        expected = [
            {"content": "\nz\n", "header_type": "h1", "title": "Cover Page", "id": None},
            {
                "content": "\na\n",
                "children": [
                    {
                        "content": "\nb\n",
                        "children": [{"content": "\nc\n", "header_type": "h3", "title": "Heading 1-2-3", "id": None}],
                        "header_type": "h2",
                        "title": "Heading 1-2",
                        "id": None,
                    }
                ],
                "header_type": "h1",
                "title": "Heading 1",
                "id": None,
            },
            {"content": "\nd\n", "header_type": "h1", "title": "Heading 1.2", "id": None},
            {
                "content": "\ne\n",
                "children": [{"content": "\nf\n", "header_type": "h2", "title": "Heading 1.3-2", "id": None}],
                "header_type": "h1",
                "title": "Heading 1.3",
                "id": None,
            },
        ]
        self.assertEqual(splitter.split(), expected)

    def test_table_split(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("tables.html"))
        self.assertEqual(splitter.split(), EXPECTED_TABLES_HEADER)

    def test_split_example(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("example.html"))
        expected = {
            "title": "Mentions légales",
            "content": """
<blockquote>
<p><span id="_Refe94959a88d0482b88316b858f9aa3f4e" class="anchor"></span>Sous réserve de disponibilité et
    de modifications techniques.</p>
<p>Toute communication ou reproduction, diffusion et/ou modification de ce document ainsi que toute exploitation ou
    communication de son contenu sont interdites, sauf autorisation expresse. Tout manquement à cette règle est
    illicite et expose son auteur au versement de dommages et intérêts. Tous les droits sont réservés en cas de
    délivrance d’un brevet, d’enregistrement d’un modèle d’utilité ou d’un modèle de design.</p>
<p>Edité par</p>
<p>Siemens Switzerland Ltd.</p>
<p>Building Technologies Division</p>
<p>International Headquarters</p>
<p>Gubelstrasse 22</p>
<p>CH-6301 Zug</p>
<p>Tel. +41 41 724-2424</p>
<p>www.siemens.com/buildingtechnologies</p>
<p>Edition: 2015-12-15</p>
<p>ID document: 009026_h_fr_--<br />
<br />
© Siemens Switzerland Ltd, 2006</p>
</blockquote>
""",
            "header_type": "h1",
            "id": "mentions-légales",
        }
        self.assertEqual(splitter.split()[1], expected)

    def test_disgusting_mammoth_output(self):
        h1_title = (
            '<a id="_Toc126736820"></a><a id="_Toc127339768"></a><a id="_Toc315192142"></a>'
            '<a id="_Toc424140850"></a>Stellsignal stetig (AO 0-10V)'
        )
        h2_title = (
            '<a id="_Toc126736819"></a><a id="_Toc127339767"></a>'
            '<a id="_Toc315192141"></a><a id="_Toc424140849"></a>Analoge Ausgänge'
        )
        expected = [
            {
                "content": "",
                "children": [
                    {
                        "content": "",
                        "header_type": "h2",
                        "title": "Stellsignal stetig (AO 0-10V)",
                        "id": "_Toc126736820",
                    }
                ],
                "header_type": "h1",
                "title": "Analoge Ausgänge",
                "id": "_Toc126736819",
            }
        ]
        headers = HtmlSplitter("<h1>%s</h1><h2>%s</h2>" % (h2_title, h1_title)).split()
        self.assertEqual(headers, expected)

    def test_malformed(self):
        expected = [
            {"content": "\nIntroduction\n\n", "header_type": "h3", "title": "Cover Page", "id": None},
            {
                "title": "Heading 3",
                "header_type": "h3",
                "content": "\na\n",
                "children": [{"title": "Heading 6", "header_type": "h6", "content": "\nb\n", "id": None}],
                "id": None,
            },
        ]
        for file in ["malformed.html", "malformed2.html"]:
            headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath(file)).split()
            self.assertEqual(headers, expected, "In {}".format(file))
        expected[1]["content"] = '\na\n</body class="page-background">\n<h6>Heading 6</h6>\nb\n'
        del expected[1]["children"]
        headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("malformed3.html")).split()
        self.assertEqual(headers, expected)

    def test_convoluted(self):
        headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("convoluted_javascripted.html")).split()
        expected = [
            {
                "title": "Problem description",
                "header_type": "h1",
                "content": "\n\nThe problem is that poeple create shitty base HTML.\n\n",
                "children": [
                    {
                        "content": "\n\nThen they format it properly...\n\n",
                        "header_type": "h4",
                        "title": "What is wrong... ",
                        "id": "statement",
                    },
                    {
                        "content": "\n\n... with javascript and CSS.\n\n",
                        "header_type": "h3",
                        "title": "...with semantic HTML ?",
                        "id": None,
                    },
                ],
                "id": "firstone",
            },
            {
                "title": "Result",
                "header_type": "h1",
                "content": "\n\nWell shit goes in, shit comes out !\n\n",
                "id": None,
            },
        ]
        self.assertEqual(headers, expected)

    def test_real_world_example(self):
        headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("iphone5repare.html")).split()
        h1s = [h for h in headers if h["header_type"] == "h1"]
        self.assertEqual(len(h1s), 2)
        h2s = h1s[1]["children"]
        h3s = []
        number_of_h2 = 0
        number_of_h2_children = 0
        number_of_h3 = 0
        for supposedly_h2 in h2s:
            if supposedly_h2["header_type"] == "h2":
                h3s += supposedly_h2.get("children", [])
                number_of_h2 += 1
        self.assertEqual(number_of_h2, 31)
        for supposedly_h3 in h3s:
            number_of_h2_children += 1
            if supposedly_h3["header_type"] == "h3":
                number_of_h3 += 1
        self.assertEqual(number_of_h2_children, 44)
        self.assertEqual(
            [h["title"] for h in h3s],
            ["Outils", "Pièces"]
            + ["Ajouter un commentaire"] * 10
            + ["Kits pour Nintendo Switch\n"] * 2
            + ["Ajouter un commentaire"] * 19
            + [
                "+13                  ",
                "Auteur\n",
                "Équipe",
                "209 commentaires         ",
                "Intégrer ce tutoriel",
                "Aperçu",
                "iFixit",
                "Boutiques",
                "Réparabilité",
                "Plaidoyer",
                "Restez au courant",
            ],
        )
        for header in headers:
            if header["header_type"] == "h1":
                first_h1 = header
        self.assertEqual(first_h1.get("title"), "Comment remplacer la batterie de l'iPhone 5s")
        self.assertEqual(first_h1.get("header_type"), "h1")
        h2s_of_first_h1 = first_h1.get("children")
        self.assertEqual(len(h2s_of_first_h1), 32)
        self.assertEqual(h2s_of_first_h1[4].get("title"), "\nÉtape 2\n\n")

    def test_anchor(self):
        headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("anchor.html")).split()
        expected = [
            {"content": "\n\nIntroduction\n\n", "header_type": "h1", "title": "Cover Page", "id": None},
            {
                "content": '\n\nHeading 1\n\n<a href="heading2"></a>\n\n',
                "header_type": "h1",
                "title": "Heading 1",
                "id": "heading1",
            },
            {
                "content": """

Heading 2

<a href="heading1"></a>

<a href="https://google.com/#Heading2">Clique</a>

""",
                "header_type": "h1",
                "title": "Heading 2",
                "id": "heading2",
            },
        ]
        self.assertEqual(headers, expected)

    def test_anchor_multiple_id(self):
        headers = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("anchor_multiple_id.html")).split()
        expected = [
            {"content": "\n\nIntroduction\n\n", "header_type": "h1", "title": "Cover Page", "id": None},
            {
                "content": "\n"
                "\n"
                "Heading 1\n"
                "\n"
                '<a href="heading1.1"></a>\n'
                '<a href="heading1.1"></a>\n'
                '<a href="heading1.1"></a>\n'
                "\n"
                "\n",
                "header_type": "h1",
                "title": "Heading 1\n    \n\n",
                "id": "heading1.1",
            },
            {
                "content": "\n"
                "\n"
                "Heading 2\n"
                "\n"
                '<a href="heading2.1"></a>\n'
                '<a href="heading2.1"></a>\n'
                '<a href="heading2.1"></a>\n'
                "\n",
                "header_type": "h1",
                "title": "Heading 2\n    \n\n",
                "id": "heading2.1",
            },
        ]
        self.assertEqual(headers, expected)
