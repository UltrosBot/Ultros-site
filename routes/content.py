__author__ = 'Gareth Coles'

import datetime

from bottle import route
from bottle import mako_template as template


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/", "GET", self.index)

    def index(self):
        db = self.manager.mongo
        bots = db.get_collection("bots")

        now = datetime.datetime.utcnow()
        last_online = now - datetime.timedelta(minutes=10)

        online = bots.find({
            "last_seen": {"$gt": last_online}
        }).count()

        return template("templates/index.html", online=online)
