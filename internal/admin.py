__author__ = 'Gareth Coles'

from bottle import request
from util import log

class AdminRoutes(object):

    def __init__(self, app):
        self.app = app

        log("Admin routes set up.")
