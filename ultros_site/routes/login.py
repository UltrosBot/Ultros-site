# coding=utf-8
import base64
import datetime
import hashlib
import secrets

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.session import Session
from ultros_site.database.schema.user import User
from ultros_site.decorators import check_csrf, add_csrf
from ultros_site.message import Message

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
        params = {}

        if not req.get_param("username", store=params) or not req.get_param("password", store=params):
            return self.render_template(
                req, resp, "login.html",
                message=Message("danger", "Login failed", "Please enter both a username and password."),
                csrf=resp.csrf
            )

        params["password"] = base64.b64encode(hashlib.sha256(params["password"].encode("utf-8")).digest())

        db_session = req.context["db_session"]

        try:
            user = db_session.query(User).filter_by(username=params["username"]).one()
        except NoResultFound:
            return self.render_template(
                req, resp, "login.html",
                message=Message("danger", "Login failed", "Incorrect username or password - please try again."),
                csrf=resp.csrf
            )
        else:
            if not bcrypt.checkpw(params["password"], user.password):
                return self.render_template(
                    req, resp, "login.html",
                    message=Message("danger", "Login failed", "Incorrect username or password - please try again."),
                    csrf=resp.csrf
                )
            if not user.email_verified:
                return self.render_template(
                    req, resp, "login.html",
                    message=Message(
                        "danger",
                        "Login failed",
                        "This user account has not been verified - please check your email for more information, or "
                        "contact one of the developers for help."
                    ),
                    csrf=resp.csrf
                )
            # Login is OK!
            token = secrets.token_urlsafe(32)
            expires = datetime.datetime.now() + datetime.timedelta(days=30)

            session = Session(user=user, token=token, expires=expires, awaiting_mfa=False)  # TODO: MFA
            db_session.add(session)

            req.set_cookie("token", token, expires=expires)
            req.context["user"] = user

            return self.render_template(
                req, resp, "index.html",
                message=Message("info", "Logged in", "You have been logged in successfully."),
            )
