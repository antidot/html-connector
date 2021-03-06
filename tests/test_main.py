import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from antidot.connector.html.main import run

BASE_WITHOUT_PASSWORD = ["xtoFt", "--login", "login", "--url", "my.fluidtopic.futile"]
BASE = ["xtoFt", "--login", "login", "--url", "my.fluidtopic.futile", "--password", "p@ssword"]
CONVERTER_OPTION = ["--converter"]
HERE = Path(__file__).parent
VERBOSE_OPTION = ["--verbose"]
FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")
NAMES = ["heading", "headings", "simple_headings", "tables"]
HTML_NAMES = ["{}.html".format(n) for n in NAMES + ["example", "title_with_tags"]]

HTML_PATHS = [Path(FIXTURE_PATH, name) for name in HTML_NAMES]


def mock_getpass(prompt):
    print(prompt)
    return "getpasspassword"


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_sysargv = sys.argv

    def tearDown(self) -> None:
        sys.argv = self.temp_sysargv

    def test_file_do_not_exists(self):
        docx_name = "mydoc.docx"
        sys.argv = BASE + [docx_name] + VERBOSE_OPTION
        with self.assertRaises(FileNotFoundError):
            run()
        sys.argv = BASE + [docx_name]
        with self.assertRaises(FileNotFoundError) as e:
            run()
        self.assertIn("[Errno 2] No such file or directory: '{}'".format(docx_name), str(e.exception))

    def test_main_html(self):
        for html_path in HTML_PATHS:
            sys.argv = BASE + [str(html_path)] + VERBOSE_OPTION
            with self.assertRaises(requests.exceptions.MissingSchema):
                fail_msg = "Problem during the treatment of {}.".format(html_path)
                self.assertEqual(run(), None, fail_msg)

    @patch("getpass.getpass", mock_getpass)
    def test_password(self):
        sys.argv = BASE_WITHOUT_PASSWORD + ["path"]
        with self.assertRaises(FileNotFoundError) as e:
            run()
        self.assertIn("[Errno 2] No such file or directory: 'path'", str(e.exception))

    def test_cover_page(self):
        sys.argv = BASE + [str(HTML_PATHS[0]), "--render-cover-page"]
        with self.assertRaises(requests.exceptions.MissingSchema):
            self.assertEqual(run(), None, "Problem with --render-cover-page")
