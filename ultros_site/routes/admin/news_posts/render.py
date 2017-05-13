# coding=utf-8
from ultros_site.base_route import BaseRoute
from ultros_site.decorators import check_admin
from ultros_site.markdown import Markdown

__author__ = "Gareth Coles"


class RenderNewsRoute(BaseRoute):
    route = "/admin/news/render"

    @check_admin
    def on_post(self, req, resp):
        params = {}

        resp.content_type = "text/html"

        if not req.get_param("markdown", store=params):
            resp.body = "<h1 class=\"title\">Error: No markdown submitted!</h1>"
        else:
            try:
                markdown = Markdown(params["markdown"])
                resp.body = markdown.html
            except Exception as e:
                resp.body = "<h1 class=\"title\">Error during parsing</h1><p>{}</p>".format(e)
