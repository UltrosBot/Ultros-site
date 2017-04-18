# coding=utf-8
import logging

__author__ = "Gareth Coles"
log = logging.getLogger("HTTP")


class OutputRequestsMiddleware:
    def __init__(self):
        log.info("Debug mode enabled")

    def process_response(self, req, resp, resource, req_succeeded):
        try:
            if " " in resp.status:
                status_code = int(resp.status.split(" ", 1)[0])
            else:
                status_code = int(resp.status)
        except Exception as e:
            log.warning(
                "Unable to parse status code from `{}`: {}".format(
                    resp.status, e
                )
            )
        else:
            log.info(
                "{:<3} | {} {}".format(
                    status_code, req.method, req.relative_uri
                )
            )
