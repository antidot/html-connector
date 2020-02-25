import logging
import os
from pathlib import Path

import requests
from fluidtopics.connector import EditorialType, Metadata, Publication, PublicationBuilder, StructuredContent

from antidot.connector.html.html_splitter_by_header import HtmlSplitterByHeader
from antidot.connector.html.html_to_topics import HtmlToTopics

LOGGER = logging.getLogger(__name__)
try:
    # pylint: disable=import-error
    from ftml.builders.topic import TopicBuilder
    from ftml.converters.publication import PublicationConverter
    from ftml.workflow.topics_splitter import TopicsSplitter

    FTML_AVAILABLE = True
except ImportError:
    FTML_AVAILABLE = False


def html_to_fluid_api(html_path: str, title: str, use_ftml: bool, metadatas: []) -> Publication:
    contents = {}
    if str(html_path).startswith("https:/") or str(html_path).startswith("http:/"):
        html_content, name = get_html_from_url(html_path)
        contents[name] = html_content
    elif Path(html_path).is_dir():
        for dirpath, _, filenames in os.walk(html_path):
            for filename in filenames:
                if filename.endswith(".html") or filename.endswith(".htm"):
                    html_absolute_path = os.path.join(dirpath, filename)
                    html_content, name = get_html_from_path(html_absolute_path, metadatas)
                    contents[name] = html_content
    else:
        html_content, name = get_html_from_path(html_path, metadatas)
        contents[name] = html_content
    publications = []
    for name, content in contents.items():
        print("adding {} with content {}".format(name, content))
        publication = get_publications_from_content(content, metadatas, name, title, use_ftml)
        publications.append(publication)
    return publications


def get_publications_from_content(html_content, metadatas, name, title, use_ftml):
    new_metadatas = []
    for metadata in metadatas:
        if metadata.key == "ft:forcedOriginId":
            LOGGER.debug("Forcing the origin ID to '%s'.", metadata.first_value)
            name = metadata.first_value
        else:
            new_metadatas.append(metadata)
    content = ft_content_from_html_content(html_content, title, use_ftml)
    publication_builder = PublicationBuilder().id(name).base_id(name).title(title).content(content)
    for metadata in new_metadatas:
        publication_builder.add_metadata(metadata)
    publications = publication_builder.build()
    return publications


def ft_content_from_html_content(html_content, title, use_ftml):
    if use_ftml and not FTML_AVAILABLE:
        raise ModuleNotFoundError("Please install the FTML connector in order to use FTML.")
    if use_ftml:
        content = ftml_split(html_content, title)
    else:
        content = default_split(html_content)
    return content


def get_html_from_url(html_path):
    response = requests.get(html_path)
    response.encoding = "utf-8"
    return response.text, html_path


def get_html_from_path(html_path, metadatas):
    html_path = Path(html_path)
    with open(html_path, "r") as html:
        html_content = html.read()
    name = "{}-{}".format(html_path.name, "-".join([str(m) for m in metadatas]))
    return html_content, name


def default_split(html_content):
    splitter = HtmlSplitterByHeader(content=html_content)
    toc_nodes = HtmlToTopics(splitter).topics
    content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content


def ftml_split(html_content, title):
    topic = TopicBuilder().title(Metadata.title(title)).content(html_content).origin_id("0").build()
    topics = [TopicsSplitter().split(topic)]
    toc_nodes = PublicationConverter().convert_toc(topics)
    content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content
