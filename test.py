import argparse
import getpass

from fluidtopics.connector import (
    EditorialType,
    LoginAuthentication,
    PublicationBuilder,
    RemoteClient,
    StructuredContent,
)

from antidot.connector.html.html_to_topics import NeoTopic

#   from fluidtopics.connector import    TocNode,    Topic,    Body,


def send_to_ft(url, login, password, source_id, publications):
    client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
    client.publish(publications)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="The remote FT url", required=True)
    parser.add_argument("--login", help="The login associated with the remote url", required=True)
    parser.add_argument("--password", help="The password associated with the remote url", required=False)
    parser.add_argument("--verbose", help="Verbosity of the logging", dest="verbose", action="store_true")
    parser.add_argument("--no-verbose", help="Verbosity of the logging", dest="verbose", action="store_false")
    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass(
            "Please enter the password for {} with login {}:\n".format(args.url, args.login)
        )
    return args


def run():
    """
    HTML:
<!DOCTYPE html>
<html>
<body>
<h1>Heading 1</h1>
a
<h2>Heading 1-2</h2>
b
<h3>Heading 1-2-3</h3>
c
<h1>Heading 1.2</h1>
d
<h1>Heading 1.3</h1>
e
<h2>Heading 1.3-2</h2>
f
</body>
</html>


    toc_nodes_ft = [
        TocNode(
            Topic(id="1", title="Heading 1", body=Body("<div>\na\n</div>")),
            children=[
                TocNode(
                    topic=Topic(id="2", title="Heading 1-2", body=Body("<div>\nb\n</div>")),
                    children=[TocNode(topic=Topic(id="3", title="Heading 1-2-3", body=Body("<div>\nc\n</div>")))],
                )
            ],
        ),
        TocNode(Topic(id="4", title="Heading 1.2", body=Body("<div>\nd\n</div>")), children=[]),
        TocNode(
            Topic(id="5", title="Heading 1.3", body=Body("<div>\ne\n</div>")),
            children=[TocNode(Topic(id="6", title="Heading 1.3-2", body=Body("<div>\nf\n</div>")))],
        ),
    ]
    """
    title = "Test simple headings"
    name = title
    toc_nodes = [
        NeoTopic(
            title="Heading 1",
            content="\na\n",
            children=[
                NeoTopic(
                    title="Heading 1-2", content="\nb\n", children=[NeoTopic(title="Heading 1-2-3", content="\nc\n")]
                )
            ],
        ),
        NeoTopic(title="Heading 1.2", content="\nd\n"),
        NeoTopic(title="Heading 1.3", content="\ne\n", children=[NeoTopic(title="Heading 1.3-2", content="\nf\n")]),
    ]
    args = parse_args()
    content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    publication_builder = PublicationBuilder().id(name).base_id(name).title(title).content(content)
    publications = publication_builder.build()
    send_to_ft(args.url, args.login, args.password, "external", publications)


if __name__ == "__main__":
    run()
