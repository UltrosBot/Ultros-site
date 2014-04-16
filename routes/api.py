__author__ = 'Gareth Coles'


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/api", "GET", self.api_index)
        app.route("/api/", "GET", self.api_index)

    def api_index(self):
        return {"routes": self.manager.api_routes}
