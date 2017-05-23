# coding=utf-8
import secrets

from falcon import HTTPBadRequest

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.backup_code import BackupCode
from ultros_site.decorators import add_csrf, check_csrf
from ultros_site.message import Message
from ultros_site.tasks.__main__ import app as celery

__author__ = "Gareth Coles"


class MFANewCodesRoute(BaseRoute):
    route = "/mfa/new_codes"

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
            req, resp, "mfa/confirm_codes.html"
        )

    @check_csrf
    @add_csrf
    def on_post(self, req, resp):
        user = req.context["user"]
        db_session = req.context["db_session"]

        db_session.query(BackupCode).filter_by(user=user).delete(synchronize_session="fetch")

        backup_codes = []

        for i in range(10):
            token = secrets.token_urlsafe(24)
            db_session.add(BackupCode(user=user, code=token))
            backup_codes.append(token)

        celery.send_task(
            "send_email",
            args=["backup_codes", user.email, "MFA backup codes"],
            kwargs={"codes": backup_codes}
        )

        resp.append_header("Refresh", "5;url=/settings")

        return self.render_template(
            req, resp, "message_gate.html",
            gate_message=Message(
                "success", "New codes generated",
                "New backup codes have been emailed to you."
            ),
            redirect_uri="/settings"
        )
