# coding=utf-8
import logging
import secrets

from falcon import HTTPBadRequest

__author__ = "Gareth Coles"
log = logging.getLogger("Decorators")


def check_csrf(func):
    def inner(self, req, *args, **kwargs):
        cookies = []
        cookies_string = req.get_header("Cookie")

        for cookie in cookies_string.split("; "):
            left, right = cookie.split("=", 1)

            if left == "_csrf":
                cookies.append(right)

        if not cookies:
            log.debug("Missing CSRF token from cookies")
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The request is missing a CSRF token."
            )

        post_token = req.get_param("_csrf")

        if post_token is None:
            log.debug("Missing CSRF token from form")
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The request is missing a CSRF token."
            )

        if post_token not in cookies:
            log.debug("CSRF tokens don't match")
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The CSRF tokens do not match."
            )

        func(self, req, *args, **kwargs)
    return inner


def add_csrf(func):
    def inner(self, req, resp, *args, **kwargs):
        token = secrets.token_urlsafe(32)

        resp.set_cookie("_csrf", token, secure=False)
        resp.csrf = token

        func(self, req, resp, *args, **kwargs)
    return inner
