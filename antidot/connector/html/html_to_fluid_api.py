import logging
import os
from pathlib import Path
from typing import Optional

import requests
from fluidtopics.connector import (
    EditorialType,
    Metadata,
    Publication,
    PublicationBuilder,
    StructuredContent,
    UnstructuredContent,
)

from antidot.connector.generic.constants import ORIGIN_ID_MAX_SIZE
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


def html_to_fluid_api(html_path: str, use_ftml: Optional[bool] = False, metadatas: Optional[list] = None):
    if metadatas is None:
        metadatas = []
    title = Path(html_path).name.replace(".html", "")
    new_metadatas = []
    for metadata in metadatas:
        if metadata.key == "ft:forcedTitle":
            title = metadata.first_value
        else:
            new_metadatas.append(metadata)
    contents = get_html_content(html_path, new_metadatas)
    publications = publication_from_html_content(contents, new_metadatas, title, use_ftml)
    return publications


def get_html_content(html_path, metadatas) -> {}:
    contents = {}
    is_an_url = str(html_path).startswith("https:/") or str(html_path).startswith("http:/")
    is_dir = Path(html_path).is_dir()
    if is_an_url:
        response = requests.get(html_path)
        response.encoding = "utf-8"
        contents[html_path] = response.text
    elif is_dir:
        for dirpath, _, filenames in os.walk(html_path):
            for filename in filenames:
                if filename.endswith(".html") or filename.endswith(".htm"):
                    html_absolute_path = os.path.join(dirpath, filename)
                    html_content, name = get_html_from_path(html_absolute_path, metadatas)
                    contents[name] = html_content
    else:
        # Is a file
        html_content, name = get_html_from_path(html_path, metadatas)
        contents[name] = html_content
    return contents


def publication_from_html_content(contents, metadatas, title, use_ftml) -> [Publication]:
    publications = []
    for name, content in contents.items():
        new_metadatas = []
        found_origin_id = False
        for metadata in metadatas:
            if metadata.key == "ft:forcedOriginId":
                LOGGER.debug("Forcing the origin ID to '%s'.", metadata.first_value)
                name = metadata.first_value
                found_origin_id = True
            else:
                new_metadatas.append(metadata)
        if logging.WARNING and not found_origin_id:
            LOGGER.warning(
                "We used a default origin_id based on the file name and its metadatas."
                " Sending the same file with the same metadata will replace it."
            )
        content, ressources = ft_content_from_html_content(content, title, use_ftml)
        publication_builder = PublicationBuilder().id(name).base_id(name).title(title).content(content)
        for ressource in ressources:
            publication_builder.resource_bank().add(ressource)
        for metadata in new_metadatas:
            publication_builder.add_metadata(metadata)
        publication = publication_builder.build()
        publications.append(publication)
        for ressource in ressources:
            publications.append(ressource)
    return publications


def ft_content_from_html_content(html_content, title, use_ftml):
    if use_ftml and not FTML_AVAILABLE:
        raise ModuleNotFoundError("Please install the FTML connector in order to use FTML.")
    if use_ftml:
        topic = TopicBuilder().title(Metadata.title(title)).content(html_content).origin_id("0").build()
        topics = [TopicsSplitter().split(topic)]
        nodes = PublicationConverter().convert_toc(topics)
        content = StructuredContent(toc=nodes, editorial_type=EditorialType.DEFAULT)
        ressources = []
    else:
        splitter = HtmlSplitterByHeader(content=html_content)
        toc_nodes, ressources = HtmlToTopics(splitter).topics
        content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content, ressources


def get_html_from_path(html_path, metadatas):
    html_path = Path(html_path)
    with open(html_path, "r") as html:
        html_content = html.read()
    name = "{}-{}".format(html_path.name, "-".join(["{}={}".format(m.key, m.values) for m in metadatas]))
    hash_len = 21
    if len(name) > ORIGIN_ID_MAX_SIZE:
        name = "{}{}".format(name[: ORIGIN_ID_MAX_SIZE - hash_len], hash(name[ORIGIN_ID_MAX_SIZE - hash_len :]))
    return html_content, name
