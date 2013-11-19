# coding=utf-8
__author__ = "Gareth Coles"

import os
import random

from bottle import route, run, static_file, abort, default_app
from bottle import mako_template as template

app = default_app()


@route('/')
def index():
    files = os.listdir("static/images/logos")
    image = random.choice(files)
    fname = image.split(".")[0]
    return template("templates/index.html", title="Under construction!",
                    image=image, img_name=fname)


@route('/static/<path:path>')
def static(path):
    return static_file(path, root="static")


@route('/static/')
@route('/static')
def static_403():
    abort(403, "You may not list the static files.")

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080, server='cherrypy', reload=True)
