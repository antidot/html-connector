import logging
import os
from pathlib import Path
from typing import Optional

import pkg_resources
import requests
from fluidtopics.connector import EditorialType, Metadata, Publication, PublicationBuilder, StructuredContent

from antidot.connector.generic.constants import METADATA_SCRIPT, ORIGIN_ID_MAX_SIZE
from antidot.connector.html.html_splitter import HtmlSplitter
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


METADATA_NOT_AFFECTING_ORIGIN_ID = ["script", "style-map-hash"]


def html_to_fluid_api(
    html_path: str, use_ftml: Optional[bool] = False, metadatas: Optional[list] = None, render_cover_page=None
):
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
    publications = publication_from_html_content(
        contents, new_metadatas, title, use_ftml=use_ftml, render_cover_page=render_cover_page
    )
    return publications


def get_html_content(html_path, metadatas) -> {}:
    contents = {}
    is_an_url = str(html_path).startswith("https:/") or str(html_path).startswith("http:/")
    is_dir = Path(html_path).is_dir()
    if is_an_url:
        response = requests.get(html_path)
        response.encoding = "utf-8"
        contents[html_path] = [response.text, False]
    elif is_dir:
        for dirpath, _, filenames in os.walk(html_path):
            for filename in filenames:
                if filename.endswith(".html") or filename.endswith(".htm"):
                    html_absolute_path = os.path.join(dirpath, filename)
                    html_content, name = get_html_from_path(html_absolute_path, metadatas)
                    contents[name] = [html_content, html_absolute_path]
    else:
        # Is a file
        html_content, name = get_html_from_path(html_path, metadatas)
        contents[name] = [html_content, html_path]
    return contents


def publication_from_html_content(contents, metadatas, title, **kwargs) -> [Publication]:
    publications = []
    for name, content_and_path in contents.items():
        content, path = content_and_path[0], content_and_path[1]
        name, new_metadatas = treat_metadatas(name, metadatas)
        content, resources = ft_content_from_html_content(content, title, path=path, **kwargs)
        publication_builder = PublicationBuilder().id(name).base_id(name).title(title).content(content)
        publication_builder.resource_bank().add_all(resources)
        for metadata in new_metadatas:
            publication_builder.add_metadata(metadata)
        publication = publication_builder.build()
        publications.append(publication)
    return publications


def treat_metadatas(name, metadatas):
    found_origin_id = False
    found_script = False
    script_name = "{}-{}".format(
        "antidot-html-connector", pkg_resources.get_distribution("antidot-html-connector").version
    )
    new_metadatas = []
    for metadata in metadatas:
        if metadata.key == "ft:forcedOriginId":
            LOGGER.debug("Forcing the origin ID to '%s'.", metadata.first_value)
            name = metadata.first_value
            found_origin_id = True
        else:
            if metadata.key == METADATA_SCRIPT:
                found_script = True
                metadata = Metadata.string(METADATA_SCRIPT, ["{}-{}".format(metadata.first_value, script_name)])
            new_metadatas.append(metadata)
    if not found_script:
        new_metadatas.append(Metadata.string(METADATA_SCRIPT, [script_name]))
    if logging.WARNING and not found_origin_id:
        LOGGER.warning(
            "We used a default origin_id based on the file name and its metadatas."
            " Sending the same file with the same metadata will replace it."
        )
    return name, new_metadatas


def ft_content_from_html_content(html_content, title, use_ftml, render_cover_page, path):
    if use_ftml and not FTML_AVAILABLE:
        raise ModuleNotFoundError("Please install the FTML connector in order to use FTML.")
    if use_ftml:
        topic = TopicBuilder().title(Metadata.title(title)).content(html_content).origin_id("0").build()
        topics = [TopicsSplitter().split(topic)]
        nodes = PublicationConverter().convert_toc(topics)
        content = StructuredContent(toc=nodes, editorial_type=EditorialType.DEFAULT)
        resources = []
    else:
        if path:
            splitter = HtmlSplitter(path=path)
        else:
            splitter = HtmlSplitter(content=html_content)
        toc_nodes, resources = HtmlToTopics(splitter, render_cover_page=render_cover_page).topics
        content = StructuredContent(toc=toc_nodes, editorial_type=EditorialType.DEFAULT)
    return content, resources


def get_html_from_path(html_path, metadatas):
    html_path = Path(html_path)
    with open(html_path, "r") as html:
        html_content = html.read()
    metadatas_name = "-".join(
        ["{}={}".format(m.key, m.values) for m in metadatas if m.key not in METADATA_NOT_AFFECTING_ORIGIN_ID]
    )
    if metadatas_name:
        name = "{}-{}".format(html_path.name, metadatas_name)
    else:
        name = "{}".format(html_path.name)
    hash_len = 21
    if len(name) > ORIGIN_ID_MAX_SIZE:
        name = "{}{}".format(name[: ORIGIN_ID_MAX_SIZE - hash_len], hash(name[ORIGIN_ID_MAX_SIZE - hash_len :]))
    return html_content, name
