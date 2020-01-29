import argparse
import getpass
import logging

from copro.html_connector.html_to_published_fluid_api import html_to_published_fluid_api


def run():
    """Try to send an html file to the fluid api."""
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
    html_to_published_fluid_api(args.path, args.url, args.login, args.password, args.use_ftml)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="The path to the file you want to convert.")
    parser.add_argument("--url", help="The remote FT url", required=True)
    parser.add_argument("--login", help="The login associated with the remote url", required=True)
    parser.add_argument("--password", help="The password associated with the remote url", required=False)
    parser.add_argument(
        "--use-ftml", help="Force using the FT FTML connector", dest="use_ftml", action="store_true", default=False
    )
    parser.add_argument("--verbose", help="Verbosity of the logging", dest="verbose", action="store_true")
    parser.add_argument("--no-verbose", help="Verbosity of the logging", dest="verbose", action="store_false")
    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass(
            "Please enter the password for {} with login {}:\n".format(args.url, args.login)
        )
    return args


if __name__ == "__main__":
    run()
