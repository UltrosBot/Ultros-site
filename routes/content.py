__author__ = 'Gareth Coles'

import os
import random

from bottle import mako_template as template


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        app.route("/", "GET", self.index)

    def index(self):
        files = os.listdir("static/images/logos")
        image = random.choice(files)
        fname = image.split(".")[0]
        return template("templates/index.html", title="Under construction!",
                        image=image, img_name=fname)
