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


def publish_html_with_client(html_path: str, client: Client, **kwargs):
    return ClientAuthentication(html_to_fluid_api, client)(html_path=html_path, **kwargs)


def publish_html(
    html_path: str, url: str, login: str, password: str, source_id: Optional[str] = HTML_CONNECTOR_SOURCE_ID, **kwargs
):  # pylint: disable=too-many-arguments
    return LoginAndPasswordAuthentication(
        html_to_fluid_api, login=login, password=password, url=url, source_id=source_id
    )(html_path=html_path, **kwargs)


def run():
    """Try to send an html file to the fluid api."""
    args = parse_args()
    if args.verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
        logging.info("%s launched in semi-verbose mode", HTML_CONNECTOR_SOURCE_ID)
    elif args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("%s launched in verbose mode", HTML_CONNECTOR_SOURCE_ID)
    kwargs = get_html_connector_kwargs_options_from_args(args)
    return publish_html(args.path, **kwargs)


def add_html_connector_options_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("--url", help="The remote FT URL", required=True)
    parser.add_argument(
        "--login", help="The login associated with the remote URL", default="root@fluidtopics.com", required=True
    )
    parser.add_argument("--password", help="The password associated with the remote URL", required=False)
    parser.add_argument(
        "--use-ftml",
        help="Use the FTML connector for content splitting",
        dest="use_ftml",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--render-cover-page",
        help="Render the cover page.",
        dest="render_cover_page",
        action="store_true",
        default=False,
    )
    return parser


def get_html_connector_kwargs_options_from_args(args):
    """Take a parsed ArgumentParser and return a dict of argument."""
    if not args.password:
        args.password = getpass.getpass(
            "Please enter the password for {} with login {}:\n".format(args.url, args.login)
        )
    return {
        "url": args.url,
        "login": args.login,
        "password": args.password,
        "use_ftml": args.use_ftml,
        "render_cover_page": args.render_cover_page,
    }


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="The path to the file you want to convert.")
    parser = add_html_connector_options_to_parser(parser)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    run()
