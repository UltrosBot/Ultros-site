# coding=utf-8
import re

from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_sink import BaseSink
from ultros_site.database.schema.email_code import EmailCode
from ultros_site.message import Message

__author__ = "Gareth Coles"


class VerifyRoute(BaseSink):
    route = re.compile("/login/verify/(?P<key>.*)")

    def __call__(self, req, resp, key):
        db_session = req.context["db_session"]

        try:
            code = db_session.query(EmailCode).filter_by(code=key).one()
        except NoResultFound:
            return self.render_template(
                req, resp, "index.html",
                message=Message("danger", "Unable to verify", "Your account has expired or already been verified"),
            )
        else:
            code.user.email_verified = True
            db_session.delete(code)

            return self.render_template(
                req, resp, "index.html",
                message=Message("info", "Email verified", "You account has been verified - you may now log in."),
            )
