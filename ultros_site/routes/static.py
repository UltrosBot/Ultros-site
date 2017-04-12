# coding=utf-8
import falcon
import os
import re

from mimetypes import guess_type

from ultros_site.base_sink import BaseSink

__author__ = "Gareth Coles"
BASE_PATH = os.path.abspath("./static/")


class StaticRoute(BaseSink):
    route = re.compile("/static/(?P<filename>.*)")

    def __call__(self, req, resp, filename):
        file_path = os.path.abspath(BASE_PATH + "/" + filename)

        if not file_path.startswith(BASE_PATH):
            raise falcon.HTTPBadRequest(
                description="Invalid filename: {}".format(filename)
            )

        if not os.path.isfile(file_path):
            raise falcon.HTTPNotFound()

        content_type = guess_type(file_path)[0]

        resp.content_type = content_type

        with open(file_path, "rb") as fh:
            resp.data = fh.read()

        resp.status = falcon.HTTP_200
