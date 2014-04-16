__author__ = 'Gareth Coles'

import datetime
import json
from uuid import uuid4

from bottle import request, abort
from bottle import mako_template as template
from sqlalchemy import Integer, Sequence, Column, String, Boolean, \
    PickleType, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Bot(base):
    """
    Bot represents a row in the "bots" table. Each row represents an Ultros bot
    and its metrics.

    Columns:
    * id - Unique row ID
    * uuid - UUID used to identify the bot
    * enabled - Whether metrics are enabled for the bot
    * packages - List of installed package dicts
    * plugins - List of installed plugin dicts
    * first_seen - Date the bot was first seen
    * last_seen - Date the bot was last seen
    """

    __tablename__ = "bots"
    id = Column(Integer, Sequence('bots_id_seq'), primary_key=True)
    uuid = Column(String(36))
    enabled = Column(Boolean())
    packages = Column(PickleType())
    plugins = Column(PickleType())
    first_seen = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))

    def __init__(self, uuid, enabled=True, packages=None, plugins=None,
                 first_seen=None, last_seen=None):

        if packages is None:
            packages = []
        if plugins is None:
            plugins = []
        if first_seen is None:
            first_seen = datetime.datetime.now()
        if last_seen is None:
            last_seen = datetime.datetime.now()

        self.uuid = uuid
        self.enabled = enabled
        self.packages = packages
        self.plugins = plugins
        self.first_seen = first_seen
        self.last_seen = last_seen

    def to_dict(self):
        """
        Convert this Bot into a dict.
        """
        return {
            "enabled": self.enabled,
            "packages": self.packages,
            "plugins": self.plugins,
            "first_seen": str(self.first_seen),
            "last_seen": str(self.last_seen)
        }

    def to_json(self):
        """
        Convert this Bot into JSON.
        """

        return json.dumps(self.to_dict())

    def __repr__(self):
        return "<Bot(%s, %s, %d packages, %d plugins, %s)>" % (
            self.uuid, self.enabled, len(self.packages), len(self.plugins),
            self.first_seen
        )


class Routes(object):

    bound = False

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/api/metrics/get/uuid", "GET", self.get_uuid)
        app.route("/api/metrics/get/metrics", "GET", self.get_metrics)
        app.route("/api/metrics/get/metrics/recent", "GET",
                  self.get_metrics_recent)

        regexp = "[a-fA-F0-9]{8}-" \
                 "[a-fA-F0-9]{4}-" \
                 "4[a-fA-F0-9]{3}-" \
                 "[89aAbB][a-fA-F0-9]{3}-" \
                 "[a-fA-F0-9]{12}"
        app.route("/api/metrics/post/<uuid:re:%s>" % regexp, "POST",
                  self.post_metrics)

        map(manager.add_api_route, ["/api/metrics/get/uuid",
                                    "/api/metrics/get/metrics",
                                    "/api/metrics/get/metrics/recent",
                                    "/api/metrics/post/<uuid>"])

    def bind(self, db):
        if not self.bound:
            base.metadata.bind = db.bind
            base.metadata.create_all(self.manager.sql_engine)
            self.bound = True

    def commit(self, db):
        return db.commit()

    def index(self):
        return template("templates/index.html")

    def get_uuid(self):
        return str(uuid4())

    def get_metrics(self, db):
        self.bind(db)

        bots = db.query(Bot).all()

        return {"metrics": [bot.to_dict() for bot in bots]}

    def get_metrics_recent(self, db):
        self.bind(db)

        now = datetime.datetime.now()
        last_fortnight = now - datetime.timedelta(weeks=2)

        bots = db.query(Bot).filter(Bot.last_seen > last_fortnight).all()

        return {"metrics": [bot.to_dict() for bot in bots]}

    def post_metrics(self, uuid, db):
        self.bind(db)
        bot = db.query(Bot).filter_by(uuid=uuid).first()

        params = request.POST.get("data", None)

        if not params:
            return abort(400, json.dumps(
                {
                    "result": "error",
                    "error": "Missing 'data' parameter"
                }
            ))

        try:
            params = json.loads(params)
        except Exception as e:
            return abort(400, json.dumps(
                {
                    "result": "error",
                    "error": "Error parsing data: %s" % e
                }
            ))

        if not bot:
            bot = Bot(uuid, params["enabled"], params["packages"],
                      params["plugins"])
            db.add(bot)

            return {"result": "created",
                    "enabled": bot.enabled}

        if not params["enabled"]:
            bot.enabled = False
            bot.packages = []
            bot.plugins = []
        else:
            bot.enabled = True
            bot.packages = params["packages"]
            bot.plugins = params["plugins"]

        bot.last_seen = datetime.datetime.now()

        db.merge(bot)
        self.commit(db)

        return {"result": "updated",
                "enabled": bot.enabled}
