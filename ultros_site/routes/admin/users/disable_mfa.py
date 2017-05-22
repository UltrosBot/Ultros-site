# coding=utf-8
import re

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_sink import BaseSink
from ultros_site.database.schema.backup_code import BackupCode
from ultros_site.database.schema.user import User
from ultros_site.decorators import check_csrf, check_admin
from ultros_site.message import Message

__author__ = "Gareth Coles"


class DisableUserMFARoute(BaseSink):
    route = re.compile("/admin/users/disable_mfa/(?P<user_id>.*)")

    @check_admin
    @check_csrf
    def __call__(self, req, resp, user_id):
        user_id = int(user_id)
        db_session = req.context["db_session"]

        try:
            db_user = db_session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            resp.append_header("Refresh", "5;url=/admin/users")

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Unknown user", "User with ID <code>{}</code> not found.".format(user_id)
                ),
                redirect_uri="/admin/users"
            )
        else:
            resp.append_header("Refresh", "5;url=/admin/users")

            if db_user.mfa_token:
                for code in db_session.query(BackupCode).filter_by(user=db_user):
                    db_session.delete(code)

                db_user.mfa_token = None
                db_user.mfa_enabled = False

                return self.render_template(
                    req, resp, "admin/message_gate.html",
                    gate_message=Message(
                        "success", "MFA disabled", "You have disabled MFA for {}".format(db_user.username)
                    ),
                    redirect_uri="/admin/users"
                )
            else:
                return self.render_template(
                    req, resp, "admin/message_gate.html",
                    gate_message=Message(
                        "warning", "MFA already disabled", "That user does not have MFA enabled."
                    ),
                    redirect_uri="/admin/users"
                )
