# coding=utf-8

from bottle import route

__author__ = 'Gareth Coles'


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/api", "GET", self.api_index)
        route("/api/", "GET", self.api_index)

    def api_index(self):
        return {"routes": self.manager.api_routes}
