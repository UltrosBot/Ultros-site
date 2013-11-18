# coding=utf-8
__author__ = "Gareth Coles"

from bottle import route, run, static_file, abort, default_app
from bottle import mako_template as template

app = default_app()

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
    run(host='0.0.0.0', port=8080, server='cherrypy')
