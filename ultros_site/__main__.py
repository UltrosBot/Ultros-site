# coding=utf-8
__author__ = "Gareth Coles"

if __name__ == "__main__":
    import waitress
    import logging

    from ultros_site.app import app

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)

    waitress.serve(app, host="0.0.0.0", port=8090)
