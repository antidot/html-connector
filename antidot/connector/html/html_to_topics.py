from pathlib import Path

from fluidtopics.connector import PublicationBuilder, ResourceBuilder, UnstructuredContent

from antidot.connector.html.neo_topics import NeoTopic
from bs4 import BeautifulSoup


class HtmlToTopics:
    def __init__(self, html_splitter):
        self.path = html_splitter.path
        self.table_of_content = html_splitter.split()
        self.ressources = []

    def set_ressources_from_html(self, html):
        """Create the resource and change the HTML to include them. """
        if html is None:
            return None
        soup = BeautifulSoup(html, "lxml")
        imgs = soup.find_all("img")
        if imgs is None:
            return html
        for image in imgs:
            print(image.attrs)
            image_path = image.attrs.get("src")
            if image_path is None:
                continue
            image_path = Path(self.path).parent.joinpath(image_path)
            if not image_path.is_file():
                continue
            content = self.__get_content_from_img_src(image_path)
            """resource = (
                ResourceBuilder().resource_id("resource_id").filename("resource.txt").content(b"the UD content").build()
            )
            publication_builder = (
                PublicationBuilder().id("pub_id").title("UD title").content(UnstructuredContent("resource_id"))
            )
            publication_builder.resource_bank().add(resource)
            self.ressources += publication_builder.build()"""
        return html

    def __get_content_from_img_src(self, image_path):
        with open(image_path, "rb") as img:
            content = img.read()
        if str(image_path).startswith("data:"):
            content = image_path.split(",")[1]
        return content

    def transform_to_fluid_api(self, title, content, children=None):
        content = self.set_ressources_from_html(content)
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
        return result, self.ressources
