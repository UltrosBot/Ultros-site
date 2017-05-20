# coding=utf-8
import hashlib

from falcon.errors import HTTPBadRequest
from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class ProfileRoute(BaseRoute):
    route = "/profile"

    def on_get(self, req, resp):
        user = req.context["user"]

        if not user:
            raise HTTPBadRequest()

        self.render_template(
            req, resp, "users/profile.html",
            user=user,
            avatar="https://www.gravatar.com/avatar/{}".format(self.gravatar_hash(user.email))
        )

    def gravatar_hash(self, email: str):
        email = email.strip()
        email = email.lower()
        email = email.encode("UTF-8")

        return hashlib.md5(email).hexdigest()
