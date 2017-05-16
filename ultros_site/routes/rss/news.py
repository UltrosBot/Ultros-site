# coding=utf-8
from email.utils import format_datetime

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.news_post import NewsPost

__author__ = "Gareth Coles"


class RSSNewsRoute(BaseRoute):
    route = "/rss/news"

    def on_get(self, req, resp):
        db_session = req.context["db_session"]
        news_posts = db_session.query(NewsPost).order_by(NewsPost.posted.desc())[0:10]
        date = format_datetime(news_posts[0].posted)

        self.render_template(
            req, resp, "rss/news.xml",
            news_posts=news_posts,
            date=date
        )
