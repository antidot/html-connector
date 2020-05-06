import unittest
from unittest.mock import patch

from fluidtopics.connector import LoginAuthentication, Metadata, RemoteClient

from antidot.connector.html.main import publish_html_with_client

from .test_main import HTML_PATHS


class MockResponse:
    def __init__(self, publications):
        self.publications = publications
        self.status_code = 404
        self.content = b"erververv"


def mock_success(self, publications):
    # pylint: disable=unused-argument
    response = MockResponse(publications)
    response.status_code = 200
    return response


def mock_publish(self, publications):
    # pylint: disable=unused-argument
    return MockResponse(publications)


def mock_source_id_does_not_exists(self, publications):
    # pylint: disable=unused-argument
    response = MockResponse(publications)
    response.status_code = 404
    response.content = "{} does not exists".format("source_id").encode()
    return response


class TestPublishToClient(unittest.TestCase):
    @patch("fluidtopics.connector.RemoteClient.publish", mock_publish)
    def test_publish_without_meta(self):
        client = RemoteClient(url="url", authentication=LoginAuthentication("login", "password"), source_id="source_id")
        response = publish_html_with_client(HTML_PATHS[0], client)
        self.assertIsNotNone(response.publications)
        self.assertEqual(response.publications.id, "heading.html")
        self.assertEqual(response.publications.title, "heading")

    @patch("fluidtopics.connector.RemoteClient.publish", mock_publish)
    def test_publish_with_meta(self):
        client = RemoteClient(url="url", authentication=LoginAuthentication("login", "password"), source_id="source_id")
        origin_id = "Forced joke origin id"
        title = "THE LITTLE FORCED TITLE IN THE PRAIRIE"
        metadatas = [Metadata.string("ft:forcedTitle", [title]), Metadata.string("ft:forcedOriginId", [origin_id])]
        response = publish_html_with_client(HTML_PATHS[0], client, metadatas=metadatas)
        self.assertIsNotNone(response.publications)
        self.assertEqual(response.publications.id, origin_id)
        self.assertEqual(response.publications.title, title)
        self.assertEqual(len(response.publications.metadata), 1)

    def assert_url_works(self, client=None):
        clients = [
            RemoteClient(url="url", authentication=LoginAuthentication("login", "password"), source_id="source_id")
        ]
        if client:
            clients.append(client)
        response = publish_html_with_client("https://fr.wikipedia.org/wiki/Miracle", clients)
        self.assertIsNotNone(response.publications)
        self.assertEqual(len(response.publications.metadata), 1)

    @patch("fluidtopics.connector.RemoteClient.publish", mock_publish)
    def test_publish_url(self):
        self.assert_url_works()

    @patch("fluidtopics.connector.RemoteClient.publish", mock_success)
    def test_publish_url_success(self):
        self.assert_url_works()

    @patch("fluidtopics.connector.RemoteClient.publish", mock_source_id_does_not_exists)
    def test_publish_url_no_source_id(self):
        self.assert_url_works()

    @patch("fluidtopics.connector.RemoteClient.publish", mock_success)
    def test_multiple_client(self):
        self.assert_url_works(
            RemoteClient(url="url2", authentication=LoginAuthentication("login2", "password2"), source_id="source_id")
        )
