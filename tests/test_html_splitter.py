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
            {
                "title": "My First Heading",
                "header_type": "h1",
                "content": """

<p>My first paragraph.</p>

""",
            }
        ]
        self.assertEqual(splitter.split(), expected)

    def test_empty_title(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("empty_title.html"))
        expected = [
            {"content": "\n    a\n    \n    b\n\n    ", "header_type": "h1", "title": "Installation"},
            {"title": "Removal", "content": "\n    c\n    \n    d\n  ", "header_type": "h1"},
        ]
        self.assertEqual(splitter.split(), expected)

    def test_simple_headings(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("standard_headings.html"))
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
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("headings_simple.html"))
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
        }
        self.assertEqual(splitter.split()[0], expected)

    def test_disgusting_mammoth_output(self):
        h1_title = (
            '<a id="_Toc126736820"></a><a id="_Toc127339768"></a><a id="_Toc315192142"></a>'
            '<a id="_Toc424140850"></a>Stellsignal stetig (AO 0-10V)'
        )
        h2_title = (
            '<a id="_Toc126736819"></a><a id="_Toc127339767"></a>'
            '<a id="_Toc315192141"></a><a id="_Toc424140849"></a>Analoge Ausgänge'
        )
        splitter = HtmlSplitter("<h1>%s</h1><h2>%s</h2>" % (h2_title, h1_title))
        expected = [
            {
                "content": "",
                "children": [{"content": "", "header_type": "h2", "title": "Stellsignal stetig (AO 0-10V)"}],
                "header_type": "h1",
                "title": "Analoge Ausgänge",
            }
        ]
        self.assertEqual(splitter.split(), expected)

    def test_real_world_example(self):
        splitter = HtmlSplitter(path=Path(FIXTURE_DIR).joinpath("iphone5repare.html"))
        headers = splitter.split()
        h1s = [h for h in headers if h["header_type"] == "h1"]
        self.assertEqual(len(h1s), 1)
        h2s = h1s[0]["children"]
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
