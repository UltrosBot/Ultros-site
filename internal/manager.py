__author__ = 'Gareth'

import logging
import os
import yaml

from beaker.middleware import SessionMiddleware
from bottle import run, default_app, request, hook

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from internal.util import log_request, log


class Manager(object):

    db = {}
    sql_engine = None
    get_session = None

    def __init__(self):
        self.app = default_app()

        self.db = yaml.load(open("config/database.yml", "r"))
        self.main_conf = yaml.load(open("config/config.yml", "r"))

        self.db_uri = "%s://%s:%s@%s/%s" % (
            self.db["adapter"], self.db["username"], self.db["password"],
            self.db["host"], self.db["database"]
        )

        if "socket" in self.db and self.db["socket"]:
            log("Using unix socket for DB connection: %s" % self.db["socket"],
                logging.INFO)
            self.db_uri += "?unix_socket=%s" % self.db["socket"]

        session_opts = {
            "session.cookie_expires": True,
            "session.type": "ext:database",
            "session.url": self.db_uri,
            "session.lock_dir": "sessions/lock/",
            # "auto": True,
            "secret": self.main_conf["secret"]
        }

        @hook('before_request')
        def setup_request():
            request.session = request.environ['beaker.session']

        @hook('after_request')
        def log_all():
            log_request(request, "%s %s " % (request.method, request.fullpath),
                        logging.INFO)

        self.wrapped = SessionMiddleware(self.app, session_opts)

        self.routes = {}
        self.api_routes = []

        files = os.listdir("routes")
        files.remove("__init__.py")

        for _file in files:
            if _file.endswith(".py"):
                module = _file.rsplit(".", 1)[0]
                if module in self.main_conf.get("disabled-routes", []):
                    log("Routes module '%s' is disabled - not loading."
                        % module, logging.INFO)
                    continue
                try:
                    log("Loading routes module '%s'..." % module, logging.INFO)
                    mod = __import__("routes.%s" % module, fromlist=["Routes"])
                    self.routes[module] = mod.Routes(self.wrapped, self)
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
        return self.wrapped

    def setup_sql(self):
        try:
            engine = create_engine(self.db_uri, pool_recycle=300)
            self.sql_engine = engine
            self.get_session = sessionmaker(bind=engine)

            from internal.schemas import Bot, Obj, User

            Bot.base.metadata.create_all(engine)
            Obj.base.metadata.create_all(engine)
            User.base.metadata.create_all(engine)

        except Exception as e:
            log("Unable to set up database: %s" % e, logging.INFO)

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

        run(app=self.wrapped, host=host, port=port, server=server)
