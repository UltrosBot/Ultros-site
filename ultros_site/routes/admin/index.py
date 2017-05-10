# coding=utf-8
from falcon import HTTPForbidden

from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class IndexRoute(BaseRoute):
    route = "/admin"

    def on_get(self, req, resp):
        user = req.context["user"]

        if user and user.admin:
            self.render_template(req, resp, "admin/index.html")
        else:
            raise HTTPForbidden()
