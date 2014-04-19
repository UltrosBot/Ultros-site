__author__ = 'Gareth Coles'

import datetime
import json

from uuid import uuid4

from bottle import request, abort
from bottle import mako_template as template

from internal.schemas import Obj, Bot


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

        app.route("/metrics", "GET", self.metrics_page)
        app.route("/metrics/", "GET", self.metrics_page)

        map(manager.add_api_route, ["/api/metrics/get/uuid",
                                    "/api/metrics/get/metrics",
                                    "/api/metrics/get/metrics/recent",
                                    "/api/metrics/post/<uuid>"])

    def metrics_page(self):
        db = self.manager.get_session()

        now = datetime.datetime.now()
        last_fortnight = now - datetime.timedelta(weeks=2)
        last_online = now - datetime.timedelta(minutes=10)

        online = db.query(Bot).filter(Bot.last_seen > last_online).count()
        online_enabled = db.query(Bot).filter_by(enabled=True)\
            .filter(Bot.last_seen > last_online).count()
        recent = db.query(Bot).filter(Bot.last_seen > last_fortnight).count()
        recent_enabled = db.query(Bot).filter_by(enabled=True)\
            .filter(Bot.last_seen > last_fortnight).count()
        total = db.query(Bot).count()
        total_enabled = db.query(Bot).filter_by(enabled=True).count()
        total_disabled = db.query(Bot).filter_by(enabled=False).count()

        other_counts = self.get_counts(db)

        kwargs = {"online": online, "recent": recent, "total": total,
                  "online_enabled": online_enabled,
                  "recent_enabled": recent_enabled,
                  "total_enabled": total_enabled,
                  "total_disabled": total_disabled,
                  "packages": other_counts["package"],
                  "protocols": other_counts["protocol"],
                  "plugins": other_counts["plugin"]
                  }

        return template("templates/metrics.html", **kwargs)

    def commit(self, db):
        return db.commit()

    def add_obj(self, db, what, who):
        r = db.query(Obj).filter_by(what=what).filter_by(who=who).first()

        if not r:
            new = Obj(what, who)
            db.add(new)
            self.commit(db)

            return new.id
        return r.id

    def get_id_map(self, db):
        r = db.query(Obj).all()
        done = {}

        for e in r:
            if e.what not in done:
                done[e.what] = {}
            done[e.what][e.who] = e.id

        return done

    def get_counts(self, db):
        done = {"package": {},
                "plugin": {},
                "protocol": {}}

        objs = db.query(Obj).all()

        for e in objs:
            if e.what == "package":
                count = db.query(Bot).filter(
                    Bot.packages.like("%%|%s|%%" % e.id)
                ).count()
            elif e.what == "plugin":
                count = db.query(Bot).filter(
                    Bot.plugins.like("%%|%s|%%" % e.id)
                ).count()
            else:
                count = db.query(Bot).filter(
                    Bot.protocols.like("%%|%s|%%" % e.id)
                ).count()

            done[e.what][e.who] = count

        return done

    def get_uuid(self):
        return str(uuid4())

    def get_metrics(self):
        db = self.manager.get_session()

        try:
            start = int(request.query.get("start", 0))
        except:
            start = 0

        bots = db.query(Bot).filter_by(enabled=True).slice(start, start + 100)\
            .all()

        return {"metrics": [bot.to_dict() for bot in bots]}

    def get_metrics_recent(self):
        db = self.manager.get_session()

        try:
            start = int(request.query.get("start", 0))
        except:
            start = 0

        now = datetime.datetime.now()
        last_fortnight = now - datetime.timedelta(weeks=2)

        bots = db.query(Bot).filter_by(enabled=True)\
            .filter(Bot.last_seen > last_fortnight)\
            .slice(start, start + 100).all()

        return {"metrics": [bot.to_dict() for bot in bots]}

    def post_metrics(self, uuid):
        db = self.manager.get_session()
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

        base_str = "|%s|"

        _packages = params["packages"]
        _plugins = params["plugins"]
        _protocols = params["protocols"]

        packages = []
        plugins = []
        protocols = []

        for element in _packages:
            _id = self.add_obj(db, "package", element)
            packages.append(str(_id))

        for element in _plugins:
            _id = self.add_obj(db, "plugin", element)
            plugins.append(str(_id))

        for element in _protocols:
            _id = self.add_obj(db, "protocol", element)
            protocols.append(str(_id))

        packages = base_str % ("|".join(packages))
        plugins = base_str % ("|".join(plugins))
        protocols = base_str % ("|".join(protocols))

        if not bot:
            if not params["enabled"]:
                bot = Bot(uuid, params["enabled"], "||", "||", "||")
            else:
                bot = Bot(uuid, params["enabled"],
                          packages, plugins, protocols)
            db.add(bot)

            return {"result": "created",
                    "enabled": bot.enabled}

        if not params["enabled"]:
            bot.enabled = False
            bot.packages = "||"
            bot.plugins = "||"
            bot.protocols = "||"
        else:
            bot.enabled = True
            bot.packages = packages
            bot.plugins = plugins
            bot.protocols = protocols

        bot.last_seen = datetime.datetime.now()

        db.merge(bot)
        self.commit(db)

        return {"result": "updated",
                "enabled": bot.enabled}