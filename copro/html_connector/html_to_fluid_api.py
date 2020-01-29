from pathlib import Path

from fluidtopics.connector import EditorialType, Metadata, Publication, PublicationBuilder, StructuredContent

from copro.html_connector.html_splitter_by_header import HtmlSplitterByHeader
from copro.html_connector.html_to_topics import HtmlToTopics

try:
    # pylint: disable=import-error
    from ftml.builders.topic import TopicBuilder
    from ftml.converters.publication import PublicationConverter
    from ftml.workflow.topics_splitter import TopicsSplitter

    FTML_AVAILABLE = True
except ModuleNotFoundError:
    FTML_AVAILABLE = False


def html_to_fluid_api(html_input: str, title: str, use_ftml: bool, metadatas: []) -> Publication:
    html_path = Path(html_input)
    with open(html_path, "r") as html:
        html_content = html.read()
    name = "{}-{}".format(html_path.name, "-".join([str(m) for m in metadatas]))
    if use_ftml and not FTML_AVAILABLE:
        raise ModuleNotFoundError("Please install the FTML connector in order to use FTML.")
    if use_ftml:
        content = ftml_split(html_content, title)
    else:
        content = default_split(html_path)
    publication_builder = PublicationBuilder().id(name).base_id(name).title(title).content(content)
    for metadata in metadatas:
        publication_builder.add_metadata(metadata)
    publications = publication_builder.build()
    return publications


def default_split(html_path):
    splitter = HtmlSplitterByHeader(path=html_path)
    toc_nodes = HtmlToTopics(splitter).topics
    content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content


def ftml_split(html_content, title):
    topic = TopicBuilder().title(Metadata.title(title)).content(html_content).origin_id("0").build()
    topics = [TopicsSplitter().split(topic)]
    toc_nodes = PublicationConverter().convert_toc(topics)
    content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content
