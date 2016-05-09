# coding=utf-8

import datetime

from bottle import route
from bottle import mako_template as template

__author__ = 'Gareth Coles'


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/", "GET", self.index)
        route("/tos", "GET", self.tos)
        route("/fanart", "GET", self.fanart)

    def index(self):
        try:
            db = self.manager.mongo
            bots = db.get_collection("bots")

            now = datetime.datetime.utcnow()
            last_online = now - datetime.timedelta(minutes=10)

            online = bots.find({
                "last_seen": {"$gt": last_online}
            }).count()
        except Exception:
            online = "???"

        return template("templates/index.html", online=online)

    def tos(self):
        try:
            db = self.manager.mongo
            bots = db.get_collection("bots")

            now = datetime.datetime.utcnow()
            last_online = now - datetime.timedelta(minutes=10)

            online = bots.find({
                "last_seen": {"$gt": last_online}
            }).count()
        except Exception:
            online = "???"

        return template("templates/tos.html", online=online)

    def fanart(self):
        try:
            db = self.manager.mongo
            bots = db.get_collection("bots")

            now = datetime.datetime.utcnow()
            last_online = now - datetime.timedelta(minutes=10)

            online = bots.find({
                "last_seen": {"$gt": last_online}
            }).count()
        except Exception:
            online = "???"

        return template("templates/fanart.html", online=online)
