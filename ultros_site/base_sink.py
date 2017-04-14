# coding=utf-8

__author__ = "Gareth Coles"


class BaseSink:
    route = "/"

    def __init__(self, manager):
        self.manager = manager

    def get_args(self) -> tuple:
        return (
            self,
            self.route
        )
