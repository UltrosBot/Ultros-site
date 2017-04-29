# coding=utf-8
from ultros_site.base_route import BaseRoute
from ultros_site.decorators import check_csrf, add_csrf

__author__ = "Gareth Coles"


class LoginRoute(BaseRoute):
    route = "/login"

    @add_csrf
    def on_get(self, req, resp):
        content_type, body = self.manager.render_template(
            "login.html", error=None, csrf=resp.csrf
        )

        resp.content_type = content_type
        resp.body = body

    @check_csrf
    @add_csrf
    def on_post(self, req, resp):
        # print(req.content_type)
        # print(req.get_param("username"))
        # print(req.get_param("password"))

        content_type, body = self.manager.render_template(
            "login.html", error="The login system is currently not implemented.", csrf=resp.csrf
        )

        resp.content_type = content_type
        resp.body = body
