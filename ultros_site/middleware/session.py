# coding=utf-8
import datetime
import logging

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.database.schema.session import Session

__author__ = "Gareth Coles"
log = logging.getLogger("Sessions")


class SessionMiddleware:
    def process_request(self, req, resp):
        req.context["user_id"] = None
        req.context["username"] = None

        cookies = req.cookies

        if "token" not in cookies:
            return

        token = cookies["token"]
        db_session = req.context["db_session"]

        try:
            session_obj = db_session.query(Session).filter_by(token=token).one()
        except NoResultFound:
            pass
        else:
            now = datetime.datetime.now()

            if now > session_obj.expires:
                db_session.delete(session_obj)
                resp.unset_cookie("token")
            else:
                session_obj.expires = now + datetime.timedelta(days=30)
                req.context["user"] = session_obj.user
