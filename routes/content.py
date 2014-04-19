__author__ = 'Gareth Coles'

import datetime

from bottle import mako_template as template

from internal.schemas import Bot


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/", "GET", self.index)

    def index(self):
        db = self.manager.get_session()

        now = datetime.datetime.now()
        last_online = now - datetime.timedelta(minutes=10)
        online = int(db.query(Bot).filter(Bot.last_seen > last_online).count())

        db.close()

        return template("templates/index.html", online=online)
