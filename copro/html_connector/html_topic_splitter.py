from copro.html_connector.html_splitter import BaseHtmlSplitter, HtmlSplitter


class HtmlTopicSplitter(BaseHtmlSplitter):
    """
    Permit to split an HTML file or string recursively by their headers.
    """

    def __split(self, title, html_content, header_level=1) -> []:
        result = []
        header_tag = "h{}".format(header_level)
        next_header = "<h{}".format(header_level + 1)
        #  print("Searching for splitting with '{}'".format(header_tag))
        for header in HtmlSplitter(content=html_content, parser=self.parser).split(header_tag):
            #  print("Header:{}".format(header))
            title = header["title"]
            header["header_type"] = header_tag
            children = self.__split(title, header["content"], header_level + 1)
            if children:
                # print("Children:{}".format(children))
                content_before_children = header["content"].split(next_header)[0]
                header["content"] = [content_before_children] + children
            result.append(header)
        if result == [] and next_header in html_content:
            return [self.__split(title, html_content, header_level + 1)]
        return result

    def split(self):
        return self.__split("Faketitle", self.content)
