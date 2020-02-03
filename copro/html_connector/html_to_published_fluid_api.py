import logging
from pathlib import Path

from fluidtopics.connector import LoginAuthentication, RemoteClient

from copro.html_connector.html_to_fluid_api import html_to_fluid_api

LOGGER = logging.getLogger(__name__)


def html_to_published_fluid_api(
    html_path: str, url: str, login: str, password: str, use_ftml: bool = False, metadatas: list = None
):  # pylint: disable=too-many-arguments
    if metadatas is None:
        metadatas = []
    title = Path(html_path).name.replace(".html", "")
    publications = html_to_fluid_api(html_path, title, use_ftml, metadatas)
    send_to_ft(url, login, password, publications)


def send_to_ft(url, login, password, publications):
    source_id = "HTMLConnector"
    client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
    response = client.publish(publications)
    if response.status_code == 404 and source_id in response.content.decode("utf8"):
        if url.endswith("/"):
            url = url[:-1]
        url = "{}{}".format(url, "/admin/khub/sources")
        LOGGER.error("Please create an 'external' source with the ID '%s' here '%s'", source_id, url)
