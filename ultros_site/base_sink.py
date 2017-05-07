# coding=utf-8

__author__ = "Gareth Coles"


class BaseSink:
    route = "/"

    def __init__(self, manager):
        self.manager = manager

    @property
    def db(self):
        return self.manager.database

    def get_args(self) -> tuple:
        return (
            self,
            self.route
        )

    def render_template(self, req, resp, template, **kwargs):
        kwargs["_context"] = req.context
        content_type, body = self.manager.render_template(
            template, **kwargs
        )

        resp.content_type = content_type
        resp.body = body
