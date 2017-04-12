# coding=utf-8

__author__ = "Gareth Coles"


class BaseSink:
    route = "/"

    def __init__(self, route_mangaer):
        self.route_manager = route_mangaer

    def get_args(self) -> tuple:
        return (
            self,
            self.route
        )
