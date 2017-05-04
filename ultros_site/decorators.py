# coding=utf-8
import secrets

from falcon import HTTPBadRequest

__author__ = "Gareth Coles"


def check_csrf(func):
    def inner(self, req, *args, **kwargs):
        cookies = req.cookies

        if "_csrf" not in cookies:
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The request is missing both CSRF tokens."
            )

        cookie_token = cookies["_csrf"]
        post_token = req.get_param("_csrf")

        if post_token is None:
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The request is missing both CSRF tokens."
            )

        if cookie_token != post_token:
            raise HTTPBadRequest(
                "Missing CSRF token",
                "The request is missing both CSRF tokens."
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
