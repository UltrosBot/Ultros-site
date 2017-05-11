# coding=utf-8
import re

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_sink import BaseSink
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
                    "danger", "What?", "We couldn't find that user!"
                ),
                redirect_uri="/admin/users"
            )
        else:
            resp.append_header("Refresh", "5;url=/admin/users")

            if db_user.mfa_token:
                db_user.mfa_token = None

                return self.render_template(
                    req, resp, "admin/message_gate.html",
                    gate_message=Message(
                        "info", "Explosions!", "That user's MFA token has been deleted."
                    ),
                    redirect_uri="/admin/users"
                )
            else:
                return self.render_template(
                    req, resp, "admin/message_gate.html",
                    gate_message=Message(
                        "info", "What?", "That user does not have MFA enabled!"
                    ),
                    redirect_uri="/admin/users"
                )
