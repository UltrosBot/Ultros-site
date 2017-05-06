# coding=utf-8
import falcon
import logging
import sys

from ultros_site.middleware.database import DatabaseMiddleware
from ultros_site.middleware.error_pages import ErrorPageMiddleware
from ultros_site.middleware.output_requests import OutputRequestsMiddleware
from ultros_site.middleware.session import SessionMiddleware
from ultros_site.route_manager import RouteManager


__author__ = "Gareth Coles"

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)-10s | %(message)s",
    level=logging.DEBUG if "--debug" in sys.argv else logging.INFO
)

manager = RouteManager()

middleware = [
    DatabaseMiddleware(manager.database),
    SessionMiddleware(),
    ErrorPageMiddleware(manager),
]

if "--debug" in sys.argv:
    middleware.append(OutputRequestsMiddleware())

app = falcon.API(middleware=middleware)
app.req_options.auto_parse_form_urlencoded = True

manager.set_app(app)
manager.load_routes()

if __name__ == "__main__":
    import waitress

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)

    waitress.serve(app, host="127.0.0.1", port=8080)
