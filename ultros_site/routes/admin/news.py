# coding=utf-8
from falcon import HTTPForbidden

from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class NewsRoute(BaseRoute):
    route = "/admin/news"

    def on_get(self, req, resp):
        user = req.context["user"]

        if user and user.admin:
            self.render_template(req, resp, "admin/news.html")
        else:
            raise HTTPForbidden()
