# coding=utf-8
from ultros_site.database_manager import DatabaseManager

__author__ = "Gareth Coles"


class DatabaseMiddleware:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def process_request(self, req, resp):
        req.context["db_session"] = self.db.create_session()

    def process_response(self, req, resp, resource, req_succeeded):
        session = req.context["db_session"]

        if req_succeeded:
            session.commit()
        else:
            session.rollback()

        session.close()
        req.context["db_session"] = None
