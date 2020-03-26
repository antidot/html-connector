import logging

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


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
        table_of_content = []
        missed_content = 0
        for i, header in enumerate(body_bs4.find_all(tag)):
            # LOGGER.debug("Tag='%s' i='%s' header='%s', table_of_content='%s'", tag, i, header, table_of_content)
            title = BeautifulSoup("".join([str(h) for h in header.contents]), self.parser).get_text()
            content = self.get_raw_content(i, split_content, tag)
            if not title and i != 0:
                missed_content += 1
                table_of_content[i - missed_content][1] += content
            else:
                table_of_content.append([title, content])
        # LOGGER.warning(table_of_content)
        for i, title_content in enumerate(table_of_content):
            title, content = title_content[0], title_content[1]
            if not title:
                continue
            result.append({"title": title, "content": content})
        return result

    @staticmethod
    def get_raw_content(i, split_content, tag):
        # Cut after the closing tag
        content = split_content[i + 1]
        # Cut before the next opening tag
        content = content.split("<{}".format(tag))[0]
        if "</body>" in content:
            content = content.split("</body>")[0]
        return content
