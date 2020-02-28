import logging
from pathlib import Path

from bs4 import BeautifulSoup
from fluidtopics.connector import ResourceBuilder

from antidot.connector.html.neo_topics import NeoTopic

LOGGER = logging.getLogger(__name__)


class HtmlToTopics:
    def __init__(self, html_splitter):
        self.path = html_splitter.path
        self.table_of_content = html_splitter.split()
        self.resources = []

    def set_resources_from_html(self, html):
        """Create the resource and change the HTML to include them. """
        if html is None:
            return None
        soup = BeautifulSoup(html, "lxml")
        imgs = soup.find_all("img")
        if imgs is None:
            return html
        for image in imgs:
            #  print(image.attrs)
            image_path = image.attrs.get("src")
            if image_path is None or self.path is None:
                continue
            image_abspath = Path(self.path).parent.joinpath(image_path)
            if not image_abspath.is_file():
                src = str(image_path)
                normal_cases = ["https://", "http://", "data:"]
                if not any([src.startswith(n) for n in normal_cases]):
                    LOGGER.warning("We did not find <%s> locally", image_path)
                continue
            content = self.__get_content_from_img_src(image_abspath)
            if self.resource_already_exists(image_abspath):
                LOGGER.info("The resource for <%s> already existed.", image_abspath)
                continue
            LOGGER.debug("Creating resource for <%s>", image_abspath)
            resource = (
                ResourceBuilder().resource_id(str(image_abspath)).filename(str(image_abspath)).content(content).build()
            )
            self.resources.append(resource)
            html = html.replace(image_path, str(image_abspath))
        return html

    def resource_already_exists(self, image_path):
        for resource in self.resources:
            if str(image_path) == resource.filename:
                return True
        return False

    @staticmethod
    def __get_content_from_img_src(image_path):
        with open(image_path, "rb") as img:
            content = img.read()
        if str(image_path).startswith("data:"):
            content = image_path.split(",")[1]
        return content

    def transform_to_fluid_api(self, title, content, children=None):
        content = self.set_resources_from_html(content)
        if children is None:
            assert isinstance(content, str), "Content related to '%s' should be a string, not None" % title
            return NeoTopic(title=title, content=content)
        fluid_children = []
        for child in children:
            if not isinstance(child, dict):
                raise TypeError("Expected a dict, got '{}' a '{}'.".format(child, type(child)))
            child_title = child["title"]
            child_content = child["content"]
            grand_children = child.get("children")
            fluid_child = self.transform_to_fluid_api(child_title, child_content, grand_children)
            #  logging.debug("Created : {}\n\n".format(fluid_child))
            fluid_children.append(fluid_child)
        #  logging.debug("Final toc is : {}".format(fluid_children))
        return NeoTopic(title=title, content=content, children=fluid_children)

    @property
    def topics(self):
        result = []
        for part in self.table_of_content:
            try:
                title = part["title"]
                content = part["content"]
                children = part.get("children")
            except Exception as e:
                raise RuntimeError(
                    "Error when initializing topics treating {} in {} : {}".format(part, self.table_of_content, e)
                )
            result.append(self.transform_to_fluid_api(title=title, content=content, children=children))
            # logging.debug("Topics : {}".format(result))
        return result, self.resources
