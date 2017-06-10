# coding=utf-8
from uuid import uuid4
from ultros_site.base_route import BaseRoute

__author__ = "Gareth Coles"


class GetUUIDRoute(BaseRoute):
    route = "/api/metrics/get/uuid"

    def on_get(self, req, resp):
        resp.body = str(uuid4())
