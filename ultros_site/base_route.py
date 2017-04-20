# coding=utf-8

__author__ = "Gareth Coles"


class BaseRoute:
    route = "/"

    def __init__(self, manager):
        self.manager = manager

    @property
    def db(self):
        return self.manager.database

    def get_args(self) -> tuple:
        return (
            self.route,
            self
        )
