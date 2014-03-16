__author__ = 'Gareth Coles'

from bottle import static_file, abort
from internal.util import log


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/static/<path:path>", ["GET", "POST"], self.static)
        app.route("/static/", ["GET", "POST"], self.static_403)
        app.route("/static", ["GET", "POST"], self.static_403)

    def static(self, path):
        return static_file(path, root="static")

    def static_403(self):
        abort(403, "You may not list the static files.")
