# coding=utf-8
import falcon
import logging

from ultros_site.middleware.error_pages import ErrorPageMiddleware
from ultros_site.route_manager import RouteManager

__author__ = "Gareth Coles"

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s",
    level=logging.INFO
)

manager = RouteManager()

app = falcon.API(middleware=[
    ErrorPageMiddleware(manager)
])

manager.set_app(app)
manager.load_routes()

if __name__ == "__main__":
    import waitress

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)

    waitress.serve(app, host="127.0.0.1", port=8080)
