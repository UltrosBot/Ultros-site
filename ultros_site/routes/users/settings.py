# coding=utf-8
import base64
import hashlib
import secrets

import bcrypt
from falcon import HTTPBadRequest

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.email_code import EmailCode
from ultros_site.decorators import add_csrf, check_csrf
from ultros_site.message import Message
from ultros_site.tasks.__main__ import app as celery

__author__ = "Gareth Coles"


class SettingsRoute(BaseRoute):
    route = "/settings"

    @add_csrf
    def on_get(self, req, resp):
        user = req.context["user"]

        if not user:
            raise HTTPBadRequest()

        self.render_template(
            req, resp, "users/settings.html",
            user=user
        )

    @check_csrf
    @add_csrf
    def on_post(self, req, resp):
        params = {}
        errors = []
        updated = []

        user = req.context["user"]
        user_email = user.email

        if not req.get_param("password", store=params):
            return self.render_template(
                req, resp, "users/settings.html",
                message=Message("danger", "Missing password", "Please enter your current password to make changes."),
                user=user
            )

        params["password"] = base64.b64encode(
            hashlib.sha256(params["password"].encode("utf-8")).digest()
        )

        db_session = req.context["db_session"]

        if not bcrypt.checkpw(params["password"], user.password.encode("UTF-8")):
            return self.render_template(
                req, resp, "users/settings.html",
                message=Message("danger", "Incorrect password", "The password you entered was incorrect."),
                user=user
            )

        if not errors:
            if req.get_param("new_password", store=params):
                if not req.get_param("new_password_again", store=params):
                    errors.append("Please confirm your new password.")
                elif not params["new_password"] == params["new_password_again"]:
                    errors.append("Your new passwords do not match.")
                else:
                    password = base64.b64encode(hashlib.sha256(params["new_password"].encode("utf-8")).digest())
                    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

                    user.password = hashed_password
                    updated.append("Password")

        if not errors:
            if req.get_param("email", store=params) and params["email"]:
                key = secrets.token_urlsafe(32)
                email_code = EmailCode(
                    user=user, code=key
                )

                db_session.add(email_code)

                celery.send_task(
                    "send_email",
                    args=["email_verification", user.email, "Email verification"],
                    kwargs={"verify_url": "/login/verify/{}".format(key)}
                )

                user.email = params["email"]
                user.email_verified = False

                updated.append("Email")

        if errors:
            return self.render_template(
                req, resp, "users/settings.html",
                message=Message(
                    "danger", "Error",
                    "The following problems were found - nothing has been changed. <br /><ul>{}</ul>".format(
                        "".join("<li>{}</li>".format(error) for error in errors)
                    )
                ),
                user=user
            )

        if updated:
            resp.append_header("Refresh", "10;url=/profile")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message(
                    "info", "Updated",
                    "You have updated the following settings: {}<br />If you updated your email, "
                    "remember to verify it - or you won't be able to log in!".format(", ".join(updated))
                ),
                redirect_uri="/profile"
            )

        return self.render_template(
            req, resp, "users/settings.html",
            message=Message("warning", "No changes", "You didn't change any settings."),
            user=user
        )
