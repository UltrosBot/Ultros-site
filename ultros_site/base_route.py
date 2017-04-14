# coding=utf-8

__author__ = "Gareth Coles"


class BaseRoute:
    route = "/"

    def __init__(self, mangaer):
        self.manager = manager

    def get_args(self) -> tuple:
        return (
            self.route,
            self
        )
