# coding=utf-8
from falcon import HTTPBadRequest

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.backup_code import BackupCode
from ultros_site.decorators import add_csrf, check_csrf
from ultros_site.message import Message
from ultros_site.tasks.__main__ import app as celery

__author__ = "Gareth Coles"


class MFADisableRoute(BaseRoute):
    route = "/mfa/disable"

    @add_csrf
    def on_get(self, req, resp):
        if not req.context["user"]:
            raise HTTPBadRequest()

        if not req.context["user"].mfa_enabled:
            resp.append_header("Refresh", "5;url=/settings")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message(
                    "warning", "No MFA",
                    "You do not have MFA enabled."
                ),
                redirect_uri="/settings"
            )

        self.render_template(
            req, resp, "mfa/confirm_disable.html"
        )

    @check_csrf
    @add_csrf
    def on_post(self, req, resp):
        user = req.context["user"]
        db_session = req.context["db_session"]

        for code in db_session.query(BackupCode).filter_by(user=user):
            db_session.delete(code)

        user.mfa_enabled = False
        user.mfa_token = None

        celery.send_task(
            "send_email",
            args=["mfa_disabled", user.email, "MFA disabled"],
            kwargs={}
        )

        resp.append_header("Refresh", "5;url=/settings")

        return self.render_template(
            req, resp, "message_gate.html",
            gate_message=Message(
                "success", "MFA disabled",
                "You have disabled MFA."
            ),
            redirect_uri="/settings"
        )
