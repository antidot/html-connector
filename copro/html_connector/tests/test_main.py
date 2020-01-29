import sys
import unittest
from pathlib import Path

import requests

from copro.html_connector.main import run

BASE = ["xtoFt", "--login", "login", "--url", "my.fluidtopic.futile", "--password", "p@ssword"]
CONVERTER_OPTION = ["--converter"]
HERE = Path(__file__).parent
VERBOSE_OPTION = ["--verbose"]
FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")
NAMES = ["heading", "headings", "simple_headings", "tables"]
HTML_NAMES = ["{}.html".format(n) for n in NAMES + ["example", "title_with_tags"]]

HTML_PATHS = [Path(FIXTURE_PATH, name) for name in HTML_NAMES]


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_sysargv = sys.argv

    def tearDown(self) -> None:
        sys.argv = self.temp_sysargv

    def test_file_do_not_exists(self):
        sys.argv = BASE + ["mydoc.docx"] + VERBOSE_OPTION
        with self.assertRaises(FileNotFoundError):
            run()

    def test_main_html(self):
        for html_path in HTML_PATHS:
            sys.argv = BASE + [str(html_path)] + VERBOSE_OPTION
            with self.assertRaises(requests.exceptions.MissingSchema):
                fail_msg = "Problem during the treatment of {}.".format(html_path)
                self.assertEqual(run(), None, fail_msg)
