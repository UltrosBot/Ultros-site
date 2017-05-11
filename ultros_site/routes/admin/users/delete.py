# coding=utf-8
import re

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_sink import BaseSink
from ultros_site.database.schema.user import User
from ultros_site.decorators import check_csrf, check_admin
from ultros_site.message import Message

__author__ = "Gareth Coles"


class DeleteUserRoute(BaseSink):
    route = re.compile("/admin/users/delete/(?P<user_id>.*)")

    @check_admin
    @check_csrf
    def __call__(self, req, resp, user_id):
        user_id = int(user_id)
        current_user = req.context["user"]

        if user_id == current_user.id:
            # Don't delete yourself!
            resp.append_header("Refresh", "5;url=/admin/users")

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Seppuku", "You can't delete your own account!"
                ),
                redirect_uri="/admin/users"
            )

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
            db_session.delete(db_user)
            resp.append_header("Refresh", "5;url=/admin/users")

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "info", "Explosions!", "That user has been deleted."
                ),
                redirect_uri="/admin/users"
            )
