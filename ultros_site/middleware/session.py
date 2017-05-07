# coding=utf-8
import datetime
import logging

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.database.schema.session import Session

__author__ = "Gareth Coles"
log = logging.getLogger("Sessions")


class SessionMiddleware:
    def process_request(self, req, resp):
        if req.path.startswith("/static/"):
            log.debug("Ignoring static file request")
            return

        req.context["user"] = None

        cookies = req.cookies

        if "token" not in cookies:
            log.debug("No token present")
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
                log.debug("Expiring old session")
                db_session.delete(session_obj)
                resp.unset_cookie("token")
            else:
                log.debug("Extending session")
                session_obj.expires = now + datetime.timedelta(days=30)
                req.context["user"] = session_obj.user
