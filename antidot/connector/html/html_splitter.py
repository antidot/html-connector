from bs4 import BeautifulSoup


class BaseHtmlSplitter:

    """
    Permit to split an HTML file or string
    """

    def __init__(self, content=None, path=None, parser="lxml"):
        self.parser = parser
        self.path = None
        error_msg = "Choose {} one between <content> and <path>."
        if content and path:
            raise ValueError(error_msg.format("only"))
        if content is None and path is None:
            raise ValueError(error_msg.format("at least"))
        if content is not None:
            self.content = content
        else:
            with open(path, "r") as html:
                self.content = html.read()
            self.path = path


class HtmlSplitter(BaseHtmlSplitter):
    def split(self, tag):
        body_bs4 = BeautifulSoup(self.content, self.parser).body
        result = []
        if body_bs4 is None:
            return result
        split_content = self.content.split("</{}>".format(tag))
        for i, header in enumerate(body_bs4.find_all(tag)):
            # logging.debug("Tag='{}' header='{}'".format(tag, header))
            title = BeautifulSoup("".join([str(h) for h in header.contents]), self.parser).get_text()
            if not title:
                continue
            # Cut after the closing tag
            content = split_content[i + 1]
            # Cut before the next opening tag
            content = content.split("<{}".format(tag))[0]
            if "</body>" in content:
                content = content.split("</body>")[0]
            element = {"title": title, "content": content}
            result.append(element)
        return result
