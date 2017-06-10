# coding=utf-8
import re

from ultros_site.base_sink import BaseSink

__author__ = "Gareth Coles"

UUID_REGEX = "[a-fA-F0-9]{8}-" \
             "[a-fA-F0-9]{4}-" \
             "4[a-fA-F0-9]{3}-" \
             "[89aAbB][a-fA-F0-9]{3}-" \
             "[a-fA-F0-9]{12}"


class DestroyRoute(BaseSink):
    route = re.compile(r"/api/metrics/destroy/(?P<uuid>{})".format(UUID_REGEX))

    def on_get(self, req, resp):
        resp.content_type = "application/json"
        resp.body = "{\"result\": \"success\"}"
