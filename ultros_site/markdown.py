# coding=utf-8
import markdown2

from bs4 import BeautifulSoup

__author__ = "Gareth Coles"


class Markdown:
    def __init__(self, markdown):
        self.markdown = markdown
        html = markdown2.markdown(
            markdown, extras={
                "fenced-code-blocks": {},
                "header-ids": {},
                "html-classes": {
                    "table": "table is-bordered is-striped",
                    "h1": "title"
                },
                "target-blank-links": {},
                "tables": {}
            },
        )

        self.html = self.add_classes(html)

    def add_classes(self, html):
        soup = BeautifulSoup(html, "html.parser")
        headers = soup.find_all("h1")

        for tag in headers:
            tag["class"] = "title"

        return str(soup)
