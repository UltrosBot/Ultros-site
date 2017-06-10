# coding=utf-8
from sqlalchemy import func

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.news_post import NewsPost
from ultros_site.decorators import check_admin, add_csrf

__author__ = "Gareth Coles"


class NewsRoute(BaseRoute):
    route = "/admin/news"

    @check_admin
    @add_csrf
    def on_get(self, req, resp):
        page = req.get_param_as_int("page") or 1
        first_index = (page - 1) * 10
        last_index = page * 10

        db_session = req.context["db_session"]
        posts = db_session.query(NewsPost).order_by(NewsPost.posted.desc())[first_index:last_index]
        count = db_session.query(func.count(NewsPost.id)).scalar()
        pages = int(count / 10)

        if count % 10:
            pages += 1
        if pages < 1:
            pages = 1

        self.render_template(
            req, resp, "admin/news.html",
            page=page,
            pages=pages,
            posts=posts,
            csrf=resp.csrf
        )
