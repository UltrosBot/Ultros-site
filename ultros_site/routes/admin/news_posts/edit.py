# coding=utf-8
from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.news_post import NewsPost
from ultros_site.decorators import check_admin, add_csrf
from ultros_site.message import Message

__author__ = "Gareth Coles"


class EditNewsRoute(BaseRoute):
    route = "/admin/news/edit"

    @check_admin
    @add_csrf
    def on_get(self, req, resp):
        params = {}

        if not req.get_param("post", store=params):
            resp.append_header("Refresh", "5;url=/admin/news/")

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Missing post ID", "Please include the ID of the post you want to edit"
                ),
                redirect_uri="/admin/news"
            )

        db_session = req.context["db_session"]

        try:
            post = db_session.query(NewsPost).filter_by(id=int(params["post"])).one()
        except NoResultFound:
            resp.append_header("Refresh", "5;url=/admin/news/")

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Error", "No such post: {}".format(params["post"])
                ),
                redirect_uri="/admin/news"
            )
        else:
            self.render_template(
                req, resp, "admin/news_create.html",
                post=post
            )
