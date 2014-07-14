__author__ = 'Gareth Coles'

import datetime
import json

from uuid import uuid4

from bottle import request, abort, route, redirect
from bottle import mako_template as template

from kitchen.text.converters import to_unicode

from pymongo.collection import ObjectId
from pymongo import DESCENDING


class Routes(object):

    bound = False

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/api/metrics/get/uuid", "GET", self.get_uuid)
        route("/api/metrics/get/metrics", "GET", self.get_metrics)
        route("/api/metrics/get/metrics/recent", "GET",
              self.get_metrics_recent)

        regexp = "[a-fA-F0-9]{8}-" \
                 "[a-fA-F0-9]{4}-" \
                 "4[a-fA-F0-9]{3}-" \
                 "[89aAbB][a-fA-F0-9]{3}-" \
                 "[a-fA-F0-9]{12}"
        route("/api/metrics/post/exception/<uuid:re:%s>" % regexp, "POST",
              self.post_exception)

        route("/api/metrics/post/<uuid:re:%s>" % regexp, "POST",
              self.post_metrics)

        route("/api/metrics/destroy/<uuid:re:%s>" % regexp, "GET",
              self.destroy)

        route("/metrics", "GET", self.metrics_page)
        route("/metrics/", "GET", self.metrics_page)

        route("/metrics/exceptions", "GET", self.exceptions_form)
        route("/metrics/exceptions/", "GET", self.exceptions_form)

        route("/metrics/exceptions", "POST", self.exceptions_form_post)
        route("/metrics/exceptions/", "POST", self.exceptions_form_post)

        route("/metrics/exceptions/<uuid>/<page>", "GET",
              self.exceptions)
        route("/metrics/exceptions/<uuid>/<page>/", "GET",
              self.exceptions)

        map(manager.add_api_route, ["/api/metrics/get/uuid",
                                    "/api/metrics/get/metrics",
                                    "/api/metrics/get/metrics/recent",
                                    "/api/metrics/destroy/<uuid>",
                                    "/api/metrics/post/<uuid>"])

    def exceptions_form(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        now = datetime.datetime.utcnow()

        last_online = now - datetime.timedelta(minutes=10)
        online = bots.find({
            "last_seen": {"$gt": last_online}
        }).count()

        return template("templates/exceptions_form.html",
                        online=online, error=None)

    def exceptions_form_post(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")
        exceptions = db.get_collection("exceptions")

        now = datetime.datetime.utcnow()

        last_online = now - datetime.timedelta(minutes=10)
        online = bots.find({
            "last_seen": {"$gt": last_online}
        }).count()

        uuid = request.forms.get("uuid", None)

        if uuid is None:
            return template("templates/exceptions_form.html",
                            online=online, error="You must specify a UUID.")

        logged = exceptions.find({
            "uuid": uuid
        }).count()

        if logged < 1:
            return template(
                "templates/exceptions_form.html",
                error="No exceptions have been logged for the UUID '%s'"
                      % uuid
            )

        return redirect("/metrics/exceptions/%s/1" % uuid)

    def exceptions(self, uuid, page):
        uuid = to_unicode(uuid)
        try:
            page = int(page)
        except Exception:
            return abort(404, "Page not found")

        if page < 1:
            return abort(404, "Page not found")

        db = self.manager.mongo
        bots = db.get_collection("bots")
        exceptions = db.get_collection("exceptions")

        now = datetime.datetime.utcnow()

        last_online = now - datetime.timedelta(minutes=10)
        online = bots.find({
            "last_seen": {"$gt": last_online}
        }).count()

        logged_num = exceptions.find({
            "uuid": uuid
        }).count()

        if logged_num < 1:
            return template(
                "templates/exceptions_form.html",
                error="No exceptions have been logged for the UUID '%s'"
                      % uuid
            )

        pages = (int(logged_num) / 10)

        overhang = int(logged_num) % 10

        if overhang > 0:
            pages += 1

        start = (page * 10) - 10
        limit = 10

        if page > pages:
            return abort(404, "Page not found")

        data = exceptions.find({
            "uuid": uuid
        }, skip=start, limit=limit, sort=[("date", DESCENDING)])

        return template("templates/exceptions.html",
                        online=online, error=None,
                        cur_page=page, max_page=pages,
                        data=data, uuid=uuid)

    def prepare_document(self, data):
        del data["uuid"]
        del data["_id"]

        packages = []
        protocols = []
        plugins = []

        for x in data["packages"]:
            packages.append(self.get_obj_by_id(x)["name"])

        for x in data["protocols"]:
            protocols.append(self.get_obj_by_id(x)["name"])

        for x in data["plugins"]:
            plugins.append(self.get_obj_by_id(x)["name"])

        data["packages"] = packages
        data["protocols"] = protocols
        data["plugins"] = plugins
        return self.manager.mongo.stringify(data)

    def metrics_page(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        now = datetime.datetime.utcnow()

        last_online = now - datetime.timedelta(minutes=10)
        last_fortnight = now - datetime.timedelta(weeks=2)

        # Online

        online = bots.find({
            "last_seen": {"$gt": last_online}
        }).count()
        online_enabled = bots.find({
            "last_seen": {"$gt": last_online},
            "enabled": True
        }).count()

        # Recent

        recent = bots.find({
            "last_seen": {"$gt": last_fortnight}
        }).count()

        recent_enabled = bots.find({
            "last_seen": {"$gt": last_fortnight},
            "enabled": True
        }).count()

        # Total

        total = bots.find().count()

        total_enabled = bots.find({
            "enabled": True
        }).count()

        total_disabled = bots.find({
            "enabled": False
        }).count()

        other_counts = self.get_counts()

        kwargs = {
            "online": online, "recent": recent, "total": total,
            "online_enabled": online_enabled,
            "recent_enabled": recent_enabled,
            "total_enabled": total_enabled,
            "total_disabled": total_disabled,
            "packages": other_counts["package"],
            "protocols": other_counts["protocol"],
            "plugins": other_counts["plugin"]
        }

        return template("templates/metrics.html", **kwargs)

    def destroy(self, uuid):
        uuid = to_unicode(uuid)

        db = self.manager.mongo
        bots = db.get_collection("bots")
        exceptions = db.get_collection("exceptions")

        r = bots.find({"uuid": uuid}).count()

        if r:
            bots.delete({"uuid": uuid}, multi=True)
            exceptions.delete({"uuid": uuid}, multi=True)
            return {"result": "success"}
        return {"result": "unknown"}

    def add_obj(self, _type, _name):
        db = self.manager.mongo
        objs = db.get_collection("objs")

        r = objs.find_one({"type": _type, "name": _name})

        if not r:
            r = {"type": _type, "name": _name}
            _id = objs.insert(r)
            return _id

        return r["_id"]

    def get_obj_by_id(self, _id):
        db = self.manager.mongo
        objs = db.get_collection("objs")

        if not isinstance(_id, ObjectId):
            _id = ObjectId(_id)

        return objs.find_one({"_id": _id})

    def get_id_map(self):
        db = self.manager.mongo
        objs = db.get_collection("objs")

        r = objs.find()
        done = {}

        for e in r:
            if e["type"] not in done:
                done[e["type"]] = {}
            done[e["type"]][e["name"]] = e["_id"]

        return done

    def get_counts(self):
        done = {"package": {},
                "plugin": {},
                "protocol": {}}

        db = self.manager.mongo
        objs = db.get_collection("objs").find()
        bots = db.get_collection("bots")

        for e in objs:
            if e["type"] == "package":
                count = bots.find({
                    "packages": {"$in": [e["_id"]]}
                }).count()
            elif e["type"] == "plugin":
                count = bots.find({
                    "plugins": {"$in": [e["_id"]]}
                }).count()
            else:
                count = bots.find({
                    "protocols": {"$in": [e["_id"]]}
                }).count()

            done[e["type"]][e["name"]] = count

        return done

    def get_online(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        last_online = (
            datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        )

        return bots.find({
            "last_seen": {"$gt": last_online}
        }).count()

    def get_uuid(self):
        return str(uuid4())

    def get_metrics(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        try:
            start = int(request.query.get("start", 0))
        except Exception:
            start = 0

        r = bots.find({
            "enabled": True
        }, skip=start, limit=100)

        data = {"metrics": [self.prepare_document(bot) for bot in r]}

        return data

    def get_metrics_recent(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        try:
            start = int(request.query.get("start", 0))
        except Exception:
            start = 0

        now = datetime.datetime.utcnow()
        last_fortnight = now - datetime.timedelta(weeks=2)

        r = bots.find({
            "enabled": True,
            "last_seen": {"$gt": last_fortnight}
        }, skip=start, limit=100)

        data = {"metrics": [self.prepare_document(bot) for bot in r]}

        return data

    def post_exception(self, uuid):
        uuid = to_unicode(uuid)
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

        params["uuid"] = uuid
        params["date"] = datetime.datetime.utcnow()

        db = self.manager.mongo
        coll = db.get_collection("exceptions")

        try:
            coll.insert(params)
        except Exception as e:
            return abort(500, json.dumps(
                {
                    "result": "error",
                    "error": "Error inserting data: %s" % e
                }
            ))
        else:
            return {"result": "submitted"}

    def post_metrics(self, uuid):
        uuid = to_unicode(uuid)

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

        for part in ["packages", "plugins", "protocols", "enabled"]:
            if part not in params:
                return {
                    "result": "error",
                    "error": "Missing parameter: %s" % part
                }

        db = self.manager.mongo
        bots = db.get_collection("bots")

        bot = bots.find_one({
            "uuid": uuid
        })

        _packages = params["packages"]
        _plugins = params["plugins"]
        _protocols = params["protocols"]

        packages = set()
        plugins = set()
        protocols = set()

        for x in _packages:
            packages.add(self.add_obj("package", x))
        for x in _plugins:
            plugins.add(self.add_obj("plugin", x))
        for x in _protocols:
            protocols.add(self.add_obj("protocol", x))

        packages = list(packages)
        plugins = list(plugins)
        protocols = list(protocols)

        if not bot:
            if not params["enabled"]:
                bot = {
                    "uuid": uuid,
                    "enabled": False,
                    "packages": [],
                    "plugins": [],
                    "protocols": [],
                    "last_seen": datetime.datetime.utcnow(),
                    "first_seen": datetime.datetime.utcnow()
                }
            else:
                bot = {
                    "uuid": uuid,
                    "enabled": True,
                    "packages": packages,
                    "plugins": plugins,
                    "protocols": protocols,
                    "last_seen": datetime.datetime.utcnow(),
                    "first_seen": datetime.datetime.utcnow()
                }

            bots.insert(bot)

            return {"result": "created",
                    "enabled": params["enabled"]}

        if not params["enabled"]:
            bot["enabled"] = False
            bot["packages"] = []
            bot["plugins"] = []
            bot["protocols"] = []
        else:
            bot["enabled"] = True
            bot["packages"] = packages
            bot["plugins"] = plugins
            bot["protocols"] = protocols

        bot["last_seen"] = datetime.datetime.utcnow()

        bots.update({
            "uuid": uuid
        }, bot)

        return {"result": "updated",
                "enabled": params["enabled"]}
