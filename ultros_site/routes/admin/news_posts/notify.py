# coding=utf-8
from sqlalchemy.orm.exc import NoResultFound

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.news_post import NewsPost
from ultros_site.decorators import check_admin, add_csrf, check_csrf
from ultros_site.message import Message
from ultros_site.tasks.notify import notify_post

__author__ = "Gareth Coles"


class NotifyNewsRoute(BaseRoute):
    route = "/admin/news/notify"

    @check_admin
    @check_csrf
    @add_csrf
    def on_get(self, req, resp):
        params = {}
        resp.append_header("Refresh", "5;url=/admin/news/")

        if not req.get_param("post", store=params):
            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Missing post ID", "Please include the ID of the post you want to delete"
                ),
                redirect_uri="/admin/news"
            )

        db_session = req.context["db_session"]

        try:
            post = db_session.query(NewsPost).filter_by(id=int(params["post"])).one()
        except NoResultFound:
            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "danger", "Error", "No such post: {}".format(params["post"])
                ),
                redirect_uri="/admin/news"
            )
        else:
            notify_post(post, self.manager.database.config["notifications"]["discord"])

            return self.render_template(
                req, resp, "admin/message_gate.html",
                gate_message=Message(
                    "success", "Notifications scheduled", "Notifications for this post have been resent."
                ),
                redirect_uri="/admin/news"
            )
