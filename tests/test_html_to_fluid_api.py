import sys
import unittest
from pathlib import Path

import pkg_resources
from fluidtopics.connector import Metadata

from antidot.connector.generic.constants import METADATA_SCRIPT, ORIGIN_ID_MAX_SIZE
from antidot.connector.html.html_to_fluid_api import get_html_content, get_html_from_path, treat_metadatas

from .test_main import HTML_NAMES


class TestHtmlToFluidApi(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_sys = sys.argv
        self.script_name = "script_name"
        self.connector_version = "antidot-html-connector-{}".format(
            pkg_resources.get_distribution("antidot-html-connector").version
        )
        self.metadatas = [Metadata.string(METADATA_SCRIPT, ["this test script"])]
        sys.argv = [self.script_name, "myhtml.html"]

    def tearDown(self) -> None:
        sys.argv = self.temp_sys

    def test_get_html_from_path(self):
        """Origin id is not gigantic even with a lot of metadata"""
        metadatas = []
        for i in range(1000):
            metadatas.append(Metadata.string("i", [-i, "long"]))
        _, name = get_html_from_path(Path(__file__), metadatas)
        self.assertLess(len(name), ORIGIN_ID_MAX_SIZE)
        _, other_name = get_html_from_path(Path(__file__), metadatas[:-1])
        self.assertNotEqual(name, other_name, "Different metadatas, same origin id !")

    def test_get_html_content(self):
        contents = get_html_content(Path(__file__).parent.joinpath("fixtures/"), [])
        for name in HTML_NAMES:
            self.assertIn(name, contents.keys())

    def test_excluded_metadata_name(self):
        """We can change the script metadata without affecting the default name created from metadata"""
        _, name = get_html_from_path(Path(__file__), self.metadatas)
        _, other_name = get_html_from_path(Path(__file__), [])
        self.assertEqual(name, other_name, "The script metadata should not affect the name!")

    def test_no_metadata_script(self):
        """We add script metadata when there is nothing."""
        new_name, new_metadatas = treat_metadatas("name", [])
        expected_metadatas = [Metadata.string(METADATA_SCRIPT, {self.connector_version})]
        self.assertEqual("name", new_name)
        self.assertEqual(new_metadatas, expected_metadatas)

    def test_preexiting_metadata_script(self):
        """We add script metadata when we already have one"""
        new_name, new_metadatas = treat_metadatas("name", self.metadatas)
        expected_metadatas = [Metadata.string(METADATA_SCRIPT, {"this test script-{}".format(self.connector_version)})]
        self.assertEqual("name", new_name)
        self.assertEqual(new_metadatas, expected_metadatas)

    def test_treat_metadatas(self):
        """We change the title when we use the foredOriginId metdata. """
        forced_name = "This is the forced origin_id"
        self.metadatas.append(Metadata.string("ft:forcedOriginId", [forced_name]))
        new_name, new_metadatas = treat_metadatas("name", self.metadatas)
        expected_metadatas = [Metadata.string(METADATA_SCRIPT, {"this test script-{}".format(self.connector_version)})]
        self.assertEqual(forced_name, new_name)
        self.assertEqual(new_metadatas, expected_metadatas)
