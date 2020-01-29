from copro.html_connector.neo_topics import NeoTopic


class HtmlToTopics:
    def __init__(self, html_splitter, tag=None):
        if tag is not None:
            table_of_content = html_splitter.split(tag)
        else:
            table_of_content = html_splitter.split()
        self.table_of_content = table_of_content

    def transform_to_fluid_api(self, title, content, children=None):
        if children is None:
            assert isinstance(content, str)
            return NeoTopic(title=title, content=content)
        fluid_children = []
        for child in children:
            # logging.debug("Inside the list <{}> is a {}".format(child, type(child)))
            if isinstance(child, str):
                fluid_child = NeoTopic(title, child)
            elif isinstance(child, dict):
                # logging.debug("Child in list is a : {} : {}".format(child.__class__, child))
                child_title = child["title"]
                child_content = child["content"]
                grand_children = child.get("children")
                fluid_child = self.transform_to_fluid_api(child_title, child_content, grand_children)
            else:
                raise RuntimeError("Unexpected value for child (expected a str or dict): {}".format(child))
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
            toc = self.transform_to_fluid_api(title=title, content=content, children=children)
            if isinstance(toc, list):
                result.append(NeoTopic(title=title, content="", children=toc))
            else:
                result.append(toc)
            # logging.debug("Topics : {}".format(result))
        return result
