__author__ = 'Gareth Coles'

from bottle import mako_template as template


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/", "GET", self.index)

    def index(self):
        return template("templates/index.html")
