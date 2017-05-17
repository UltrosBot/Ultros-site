# coding=utf-8
from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.news_post import NewsPost

__author__ = "Gareth Coles"


class FeedsRoute(BaseRoute):
    route = "/feeds"

    def on_get(self, req, resp):
        self.render_template(
            req, resp, "feeds.html",
        )
