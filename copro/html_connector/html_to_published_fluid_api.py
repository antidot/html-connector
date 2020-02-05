import logging
from pathlib import Path
from typing import Optional

from fluidtopics.connector import Client, LoginAuthentication, RemoteClient

from copro.html_connector.external_source_id_does_not_exists_error import ExternalSourceIdDoesNotExistsError
from copro.html_connector.html_to_fluid_api import html_to_fluid_api

LOGGER = logging.getLogger(__name__)

HTML_CONNECTOR_SOURCE_ID = "HTMLConnector"


def html_to_published_fluid_api(
    html_path: str,
    url: Optional[str] = None,
    login: Optional[str] = None,
    password: Optional[str] = None,
    source_id: Optional[str] = HTML_CONNECTOR_SOURCE_ID,
    use_ftml: Optional[bool] = False,
    metadatas: Optional[list] = None,
    client: Optional[Client] = None,
):  # pylint: disable=too-many-arguments
    """ Publish an html file to FT. """
    if client is not None:
        if url or login or password:
            raise ValueError("Cannot use both url/login/password and a Client '{}'.".format(client))
        if source_id != HTML_CONNECTOR_SOURCE_ID:
            raise ValueError(
                "Cannot use the source_id parameter '{}' and a Client '{}' at the same time.".format(source_id, client)
            )
    if client is None:
        if not (url and login and password):
            raise ValueError("Need at least url and login and password or a Client, got neither")
        client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
    if metadatas is None:
        metadatas = []
    title = Path(html_path).name.replace(".html", "")
    publications = html_to_fluid_api(html_path, title, use_ftml, metadatas)
    send_to_ft(client, publications)


def send_to_ft(client, publications):
    response = client.publish(publications)
    if response.status_code == 404 and client.source_id in response.content.decode("utf8"):
        raise ExternalSourceIdDoesNotExistsError(client)
