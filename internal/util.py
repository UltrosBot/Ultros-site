# coding=utf-8

import logging
import sys

__author__ = 'Gareth Coles'

logging.basicConfig(
    format="%(asctime)s | %(levelname)8s | %(message)s",
    datefmt="%d %b %Y - %H:%M:%S",
    level=(logging.DEBUG if "--debug" in sys.argv else logging.INFO))


def log(message, level=logging.DEBUG):
    logging.log(level, message)


def log_request(request, message, level=logging.DEBUG):
    ip = request.remote_addr
    log("[%s] %s" % (ip, message), level)
