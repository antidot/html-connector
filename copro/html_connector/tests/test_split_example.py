import unittest
from pathlib import Path

from copro.html_connector.html_splitter_by_header import HtmlSplitterByHeader

HERE = Path(__file__).parent
FIXTURE_DIR = Path(HERE).joinpath("fixtures")


class TestSplitExample(unittest.TestCase):

    maxDiff = None

    def test_split_example(self):
        splitter = HtmlSplitterByHeader(path=Path(FIXTURE_DIR).joinpath("example.html"))
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
        splitter = HtmlSplitterByHeader("<h1>%s</h1><h2>%s</h2>" % (h2_title, h1_title))
        expected = [
            {
                "content": "",
                "children": [{"content": "", "header_type": "h2", "title": "Stellsignal stetig (AO 0-10V)"}],
                "header_type": "h1",
                "title": "Analoge Ausgänge",
            }
        ]
        self.assertEqual(splitter.split(), expected)
