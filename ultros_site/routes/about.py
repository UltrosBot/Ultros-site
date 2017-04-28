# coding=utf-8
from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class AboutRoute(BaseRoute):
    route = "/about"

    def on_get(self, req, resp):
        content_type, body = self.manager.render_template("about.html")

        resp.content_type = content_type
        resp.body = body
