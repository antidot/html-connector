"""
Permit to take an HTML document, split it according to its headers, and push it to an FT server.
"""

import argparse
import getpass
import logging
from typing import Optional

from fluidtopics.connector import Client

from antidot.connector.generic.decorators import ClientAuthentication, LoginAndPasswordAuthentication
from antidot.connector.html.html_to_fluid_api import html_to_fluid_api

LOGGER = logging.getLogger(__name__)
HTML_CONNECTOR_SOURCE_ID = "HTMLConnector"


def publish_html_with_client(
    html_path: str, client: Client, metadatas: Optional[list] = None, use_ftml: Optional[bool] = False
):
    return ClientAuthentication(html_to_fluid_api, client)(html_path=html_path, metadatas=metadatas, use_ftml=use_ftml)


def publish_html(
    html_path: str,
    url: str,
    login: str,
    password: str,
    source_id: Optional[str] = HTML_CONNECTOR_SOURCE_ID,
    use_ftml: Optional[bool] = False,
    metadatas: Optional[list] = None,
):  # pylint: disable=too-many-arguments
    return LoginAndPasswordAuthentication(
        html_to_fluid_api, login=login, password=password, url=url, source_id=source_id
    )(html_path=html_path, metadatas=metadatas, use_ftml=use_ftml)


def run():
    """Try to send an html file to the fluid api."""
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("%s launched in verbose mode", HTML_CONNECTOR_SOURCE_ID)
    else:
        logging.basicConfig(level=logging.WARNING)
    publish_html(html_path=args.path, url=args.url, login=args.login, password=args.password, use_ftml=args.use_ftml)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="The path to the file you want to convert.")
    parser.add_argument("--url", help="The remote FT url", required=True)
    parser.add_argument("--login", help="The login associated with the remote url", required=True)
    parser.add_argument("--password", help="The password associated with the remote url", required=False)
    parser.add_argument(
        "--use-ftml",
        help="Use the FTML connector for content splitting",
        dest="use_ftml",
        action="store_true",
        default=False,
    )
    parser.add_argument("--verbose", help="Verbosity of the logging", action="store_true", default=False)
    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass(
            "Please enter the password for {} with login {}:\n".format(args.url, args.login)
        )
    return args


if __name__ == "__main__":
    run()
