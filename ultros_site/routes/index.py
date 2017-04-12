# coding=utf-8
from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class IndexRoute(BaseRoute):
    route = "/"

    def on_get(self, req, resp):
        content_type, body = self.route_manager.render_template("index.html")

        resp.content_type = content_type
        resp.body = body
