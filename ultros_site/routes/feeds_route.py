# coding=utf-8
from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class FeedsRoute(BaseRoute):
    route = "/feeds"

    def on_get(self, req, resp):
        self.render_template(
            req, resp, "feeds.html",
        )
