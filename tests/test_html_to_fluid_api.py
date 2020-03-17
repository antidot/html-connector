import unittest
from pathlib import Path

from fluidtopics.connector import Metadata

from antidot.connector.generic.constants import ORIGIN_ID_MAX_SIZE
from antidot.connector.html.html_to_fluid_api import get_html_from_path


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
