# coding=utf-8
from falcon import HTTPForbidden

from ultros_site.base_route import BaseRoute
from ultros_site.decorators import check_admin

__author__ = "Gareth Coles"


class NewsRoute(BaseRoute):
    route = "/admin/news"

    @check_admin
    def on_get(self, req, resp):
        self.render_template(req, resp, "admin/news.html")
