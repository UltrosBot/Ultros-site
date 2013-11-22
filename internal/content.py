__author__ = 'Gareth Coles'

import os
import random

from bottle import request
from bottle import mako_template as template
from util import log

class ContentRoutes(object):

    def __init__(self, app):
        self.app = app

        app.route("/", "GET", self.index)

        log("Content routes set up.")

    def index(self):
        files = os.listdir("static/images/logos")
        image = random.choice(files)
        fname = image.split(".")[0]
        return template("templates/index.html", title="Under construction!",
                        image=image, img_name=fname)
