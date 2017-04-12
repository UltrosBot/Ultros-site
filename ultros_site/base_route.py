# coding=utf-8

__author__ = "Gareth Coles"


class BaseRoute:
    route = "/"

    def __init__(self, route_mangaer):
        self.route_manager = route_mangaer

    def get_args(self) -> tuple:
        return (
            self.route,
            self
        )
