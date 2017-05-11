# coding=utf-8

from ultros_site.routes.admin.index import IndexRoute
from ultros_site.routes.admin.news import NewsRoute
from ultros_site.routes.admin.users_route import UsersRoute

from ultros_site.routes.admin.users import PromoteUserRoute, VerifyUserRoute, DisableUserMFARoute, DemoteUserRoute, \
    DeleteUserRoute


__author__ = "Gareth Coles"
__all__ = [
    "IndexRoute", "NewsRoute", "UsersRoute", "PromoteUserRoute", "VerifyUserRoute", "DeleteUserRoute",
    "DemoteUserRoute", "DisableUserMFARoute"
]
