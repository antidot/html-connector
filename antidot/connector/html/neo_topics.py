from fluidtopics.connector import Body, TocNode, Topic


class NeoTopic(TocNode):
    def __init__(self, title, content, *args, children: list = None, **kwargs):
        if children is None:
            children = []
        for child in children:
            if not isinstance(child, (TocNode, NeoTopic)):
                error_msg = "Error while creating Topic '{}' with content '{}'. "
                error_msg += "We expect a list of TocNode Or NeoTopic as children, but '{}' is a '{}'"
                raise TypeError(error_msg.format(title, content, child, type(child)))
        if not isinstance(content, str):
            raise TypeError("'content' should be a str but is a {} : {}".format(type(content), content))
        content = " ".join(content.split())
        hashed_id = hash(title + content)
        super(NeoTopic, self).__init__(
            Topic(id=hashed_id, title=title, body=Body("<div>{}</div>".format(content)), *args, **kwargs),
            children=children,
        )

    def __repr__(self):
        return """<Topic>
    Title:
        {}
    Content:
        {}
    Children:
        {}
</Topic>
""".format(
            self.title, self.topic.body.html, self.children
        )

    def get_title(self):
        return self.topic.get_title()

    @property
    def id(self):
        return self.topic.id

    @property
    def title(self):
        return self.get_title()

    @property
    def base_id(self):
        return self.topic.base_id

    @property
    def variant_selector(self):
        return self.topic.variant_selector

    def get_description(self):
        return self.topic.get_description()

    def get_pretty_url(self):
        return self.topic.get_pretty_url()

    @property
    def body(self):
        return self.topic.body

    @property
    def metadata(self):
        return self.topic.metadata
