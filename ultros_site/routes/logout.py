# coding=utf-8
from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.session import Session
from ultros_site.message import Message

__author__ = "Gareth Coles"


class LoginRoute(BaseRoute):
    route = "/logout"

    def on_get(self, req, resp):
        resp.append_header("Refresh", "5;url=/")

        if not req.context["user"]:
            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message("danger", "Error", "You are not logged in"),
                redirect_uri="/"
            )

        db_session = req.context["db_session"]
        token = req.cookies["token"]

        try:
            session = db_session.query(Session).filter_by(token=token).one()
        except NoResultFound:
            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message("danger", "Error", "You are not logged in"),
                redirect_uri="/"
            )
        else:
            db_session.delete(session)
            resp.unset_cookie("token")

            return self.render_template(
                req, resp, "message_gate.html",
                gate_message=Message("info", "Logged out", "You have been logged out."),
                redirect_uri="/"
            )
