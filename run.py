# coding=utf-8
__author__ = "Gareth Coles"

from bottle import route, run, static_file, abort, Bottle
from bottle import mako_template as template


@route('/')
def index():
    return template("templates/index.html", title="Index")


@route('/static/<path:path>')
def static(path):
    return static_file(path, root="static")


@route('/static/')
def static_403():
    abort(403, "You may not list the static files.")

if __name__ == "__main__":
    run(host='localhost', port=8080, server='cherrypy')
else:
    app = application = Bottle()  # Run for uWSGI.
                                  # Otherwise, use CherryPy for the dev server.
