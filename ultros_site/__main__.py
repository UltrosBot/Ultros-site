# coding=utf-8
import falcon

from ultros_site.route_manager import RouteManager

__author__ = "Gareth Coles"

app = falcon.API()

manager = RouteManager(app)
manager.load_routes()

if __name__ == "__main__":
    import waitress
    import logging

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)

    waitress.serve(app, host="127.0.0.1", port=8080)
