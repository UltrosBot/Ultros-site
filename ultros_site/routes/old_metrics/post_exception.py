# coding=utf-8
import re

from ultros_site.base_sink import BaseSink

__author__ = "Gareth Coles"

UUID_REGEX = "[a-fA-F0-9]{8}-" \
             "[a-fA-F0-9]{4}-" \
             "4[a-fA-F0-9]{3}-" \
             "[89aAbB][a-fA-F0-9]{3}-" \
             "[a-fA-F0-9]{12}"


class PostExceptionRoute(BaseSink):
    route = re.compile(r"/api/metrics/post/exception/(?P<uuid>{})".format(UUID_REGEX))

    def __call__(self, req, resp):
        resp.content_type = "application/json"
        resp.body = "return {\"result\": \"submitted\"}"
