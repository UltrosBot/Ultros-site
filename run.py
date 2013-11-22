# coding=utf-8
__author__ = "Gareth Coles"

import logging

from bottle import run, default_app, request, hook
from internal import api, static, content, admin
from internal.util import log_request

app = default_app()

@hook('after_request')
def log_all():
    log_request(request, "%s %s " % (request.method, request.fullpath),
                logging.INFO)

admin_class = admin.AdminRoutes(app)
api_class = api.ApiRoutes(app)
content_class = content.ContentRoutes(app)
static_class = static.StaticRoutes(app)

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080, server='cherrypy', reload=True)
