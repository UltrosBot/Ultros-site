__author__ = 'Gareth'

import logging
import os
import yaml

from bottle import run, default_app, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from internal.util import log_request, log


class Manager(object):

    db = {}
    sql_engine = None
    get_session = None

    def __init__(self):
        self.app = default_app()

        def log_all():
            log_request(request, "%s %s " % (request.method, request.fullpath),
                        logging.INFO)

        self.app.hook("after_request")(log_all)

        self.routes = {}
        self.api_routes = []

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
        log("%s routes set up." % len(self.app.routes), logging.INFO)

    def add_api_route(self, route):
        if route in self.api_routes:
            return False
        self.api_routes.append(route)
        self.api_routes = sorted(self.api_routes)
        return True

    def get_app(self):
        return self.app

    def setup_sql(self):
        try:
            db_config = yaml.load(open("config/database.yml", "r"))
            self.db = db_config

            db_uri = "%s://%s:%s@%s/%s" % (
                self.db["adapter"], self.db["username"], self.db["password"],
                self.db["host"], self.db["database"]
            )

            if "socket" in self.db and self.db["socket"]:
                db_uri += "?unix_socket=%s" % self.db["socket"]

            engine = create_engine(db_uri)
            self.sql_engine = engine
            self.get_session = sessionmaker(bind=engine)

            from internal.schemas import Bot, Obj

            Bot.base.metadata.create_all(engine)
            Obj.base.metadata.create_all(engine)

        except Exception as e:
            log("Unable to load database config: %s" % e, logging.INFO)

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
