import logging
import re

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


class BaseHtmlSplitter:

    """
    Permit to split an HTML file or string
    """

    INTERNAL_BODY_FINDER = re.compile(r"<body[\w\-=\"\ ]*>([\s\S]+?)<\/body>")

    @staticmethod
    def normalize_html(html):
        return BeautifulSoup(html, "html.parser").prettify()

    @staticmethod
    def get_html_between_body(html):
        re_search = BaseHtmlSplitter.INTERNAL_BODY_FINDER.search(html)
        if re_search:
            return re_search.group(1)
        return html

    def __init__(self, content=None, path=None, parser="lxml"):
        self.parser = parser
        self.path = None
        error_msg = "Choose {} one between <content> and <path>."
        if content and path:
            raise ValueError(error_msg.format("only"))
        if content is None and path is None:
            raise ValueError(error_msg.format("at least"))
        if content is None:
            with open(path, "r") as html:
                content = html.read()
            self.path = path
        self.content = self.get_html_between_body(content)


class HtmlSplitter(BaseHtmlSplitter):
    HEADER_REGEX = re.compile(r'^h[1-7][\w\-="\ ]*')

    def split(self):
        parsed_html = BeautifulSoup(self.content, self.parser).body
        if parsed_html is None:
            return []
        split_content = self.get_split_content(parsed_html)
        result = self.create_proper_list(split_content)
        hierarchized_content = self.__get_hierarchized_content(result)
        return hierarchized_content[1:]

    def create_proper_list(self, split_content):
        result = []
        headers = set(c["header_type"] for c in self.__iter_on_split_content(split_content))
        higest_level_header = "h1" if not headers else min(headers)
        cover_page = split_content[0]
        result.append({"title": "Cover Page", "header_type": higest_level_header, "content": cover_page})
        for title_header_content in self.__iter_on_split_content(split_content):
            result.append(title_header_content)
        return result

    @staticmethod
    def __iter_on_split_content(split_content):
        split_content = iter(split_content[1:])
        while True:
            try:
                title_and_header = next(split_content)
                content = next(split_content)
                title_and_header["content"] = content
                yield title_and_header
            except StopIteration:
                return

    def __get_hierarchized_content(self, flat_headers):
        hierarchized = []
        headers = set(h["header_type"] for h in flat_headers)
        if len(headers) <= 1:
            return flat_headers
        highest_level_header = min(headers)
        father = flat_headers[0]
        children = []
        for content in flat_headers[1:]:
            if content["header_type"] == highest_level_header:
                if father != content:
                    if children:
                        father["children"] = self.__get_hierarchized_content(children)
                    hierarchized.append(father)
                children = []
                father = content
            else:
                children.append(content)
        if children:
            father["children"] = self.__get_hierarchized_content(children)
        hierarchized.append(father)
        return hierarchized

    def get_split_content(self, parsed_html):
        has_empty_title = False
        split_content = []
        after = self.content
        for tag in parsed_html.find_all(self.HEADER_REGEX):
            html_splitted_by_tag = after.split(str(tag))
            if len(html_splitted_by_tag) >= 1:
                end_tag = "</{}>".format(tag.name)
                html_splitted_manually = after.split(end_tag)
                html_splitted_by_tag[0] = html_splitted_manually[0].split("<{}".format(tag.name))[0]
                begin_tag = "<{}".format(tag.name)
                html_splitted_by_tag = [
                    html_splitted_manually[0].split(begin_tag)[0],
                    end_tag.join(html_splitted_manually[1:]),
                ]
            after = "".join(html_splitted_by_tag[1:])
            title = self.__get_text_from_tag(tag)
            if not title:
                has_empty_title = True
            split_content += [html_splitted_by_tag[0], {"title": title, "header_type": tag.name}]
        split_content.append(after)
        if has_empty_title:
            split_content = self.__remove_empty_titles(split_content)
        return split_content

    @staticmethod
    def __remove_empty_titles(split_content):
        compacted_content = []
        split_content = iter(split_content)
        current_content = next(split_content)
        try:
            while True:
                title_and_header = next(split_content)
                content = next(split_content)
                if not title_and_header["title"]:
                    current_content += content
                else:
                    compacted_content += [current_content, title_and_header]
                    current_content = content
        except StopIteration:
            compacted_content += [current_content]
        return compacted_content

    def __get_text_from_tag(self, tag):
        return BeautifulSoup("".join([str(h) for h in tag.contents]), self.parser).get_text()
