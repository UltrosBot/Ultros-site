__author__ = 'Gareth'

import logging
import os
import yaml

from bottle import run, default_app, request, hook
from internal.util import log_request, log


class Manager(object):

    def __init__(self):
        self.app = default_app()

        @hook("after_request")
        def log_all():
            log_request(request, "%s %s " % (request.method, request.fullpath),
                        logging.INFO)

        self.routes = {}

        files = os.listdir("routes")
        files.remove("__init__.py")

        for _file in files:
            if _file.endswith(".py"):
                module = _file.rsplit(".", 1)[0]
                try:
                    log("Loading routes module '%s'..." % module, logging.INFO)
                    mod = __import__("routes.%s" % module, fromlist=["Routes"])
                    self.routes[module] = mod.Routes(self.app, self)
                except Exception as e:
                    log("Error loading routes module '%s': %s" % (module, e),
                        logging.INFO)

        log("Finished loading routes modules.", logging.INFO)

    def get_app(self):
        return self.app

    def start(self):
        try:
            config = yaml.load(open("config/development.yml", "r"))
            host = config.get("host", "127.0.0.1")
            port = config.get("port", 8080)
            server = config.get("server", "cherrypy")
        except Exception as e:
            log("Unable to load development config: %s" % e, logging.INFO)
            log("Continuing using the defaults.", logging.INFO)
            host = "127.0.0.1"
            port = 8080
            server = "cherrypy"
        run(host=host, port=port, server=server)
