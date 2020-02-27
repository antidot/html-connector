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
        print(name)
        self.assertLess(len(name), ORIGIN_ID_MAX_SIZE)
        _, other_name = get_html_from_path(Path(__file__), metadatas[:-1])
        self.assertNotEqual(name, other_name, "Different metadatas, same origin id !")
