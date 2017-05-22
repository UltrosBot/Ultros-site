# coding=utf-8
import pyotp
from falcon import HTTPBadRequest

from ultros_site.base_route import BaseRoute
from ultros_site.decorators import add_csrf, check_csrf
from ultros_site.message import Message

__author__ = "Gareth Coles"


class MFAChallengeRoute(BaseRoute):
    route = "/mfa/challenge"

    @add_csrf
    def on_get(self, req, resp):
        if not req.context["user"]:
            raise HTTPBadRequest()

        if not req.context["user"].mfa_enabled:
            resp.append_header("Refresh", "5;url=/")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message(
                    "warning", "No MFA",
                    "You do not have MFA enabled."
                ),
                redirect_uri="/"
            )

        if not req.context["session"].awaiting_mfa:
            resp.append_header("Refresh", "5;url=/")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message(
                    "warning", "Already authenticated",
                    "You have already authenticated with MFA."
                ),
                redirect_uri="/"
            )

        self.render_template(
            req, resp, "mfa/challenge.html"
        )

    @check_csrf
    @add_csrf
    def on_post(self, req, resp):
        user = req.context["user"]
        totp = pyotp.TOTP(user.mfa_token)
        code = req.get_param("code")

        if not code:
            return self.render_template(
                req, resp, "mfa/challenge.html",
                message=Message(
                    "danger", "Missing code",
                    "Please enter a code from your authenticator application to continue."
                )
            )

        if totp.verify(code):
            req.context["session"].awaiting_mfa = False
            resp.append_header("Refresh", "5;url=/")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message(
                    "success", "Authenticated",
                    "You have logged in and authenticated successfully."
                ),
                redirect_uri="/"
            )
        else:
            return self.render_template(
                req, resp, "mfa/challenge.html",
                message=Message(
                    "danger", "Invalid code",
                    "The code you entered was invalid. Please try again!"
                )
            )
