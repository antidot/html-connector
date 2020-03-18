import sys
import unittest
from pathlib import Path

import pkg_resources
from fluidtopics.connector import Metadata

from antidot.connector.generic.constants import ORIGIN_ID_MAX_SIZE
from antidot.connector.html.html_to_fluid_api import get_html_from_path, treat_metadatas


class TestHtmlToFluidApi(unittest.TestCase):
    def test_get_html_from_path(self):
        """Origin id is not gigantic even with a lot of metadata"""
        metadatas = []
        for i in range(1000):
            metadatas.append(Metadata.string("i", [-i, "long"]))
        _, name = get_html_from_path(Path(__file__), metadatas)
        self.assertLess(len(name), ORIGIN_ID_MAX_SIZE)
        _, other_name = get_html_from_path(Path(__file__), metadatas[:-1])
        self.assertNotEqual(name, other_name, "Different metadatas, same origin id !")

    def test_excluded_metadata_name(self):
        """We can change the script metadata without affecting the default name created from metadata"""
        metadatas = [Metadata.string("script", ["this test script"])]
        _, name = get_html_from_path(Path(__file__), metadatas)
        _, other_name = get_html_from_path(Path(__file__), [])
        self.assertEqual(name, other_name, "The script metadata should not affect the name!")

    def test_treat_metadatas(self):
        """We add script metadata when we have one"""
        temp = sys.argv
        script_name = "script_name"
        sys.argv = [script_name, "myhtml.html"]
        connector_version = (pkg_resources.get_distribution("antidot-html-connector").version,)

        forced_name = "This is the forced origin_id"
        metadatas = [Metadata.string("script", ["this test script"])]
        found_origin_id, new_name, new_metadatas = treat_metadatas(False, metadatas, "name")
        self.assertEqual("name", new_name)
        expected_metadatas = [
            Metadata.string(
                "script", {"this test script", "{}-antidot-html-connector-{}".format(script_name, connector_version[0])}
            )
        ]
        self.assertEqual(new_metadatas, expected_metadatas)
        self.assertFalse(found_origin_id)
        metadatas.append(Metadata.string("ft:forcedOriginId", [forced_name]))
        found_origin_id, new_name, new_metadatas = treat_metadatas(False, metadatas, "name")
        self.assertEqual(forced_name, new_name)
        self.assertEqual(new_metadatas, expected_metadatas)
        self.assertTrue(found_origin_id)
        sys.argv = temp
