__author__ = 'Gareth Coles'

from bottle import request
from util import log


class ApiRoutes(object):

    def __init__(self, app):
        self.app = app

        log("API routes set up.")
