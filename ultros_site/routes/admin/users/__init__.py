# coding=utf-8
from ultros_site.routes.admin.users.delete import DeleteUserRoute
from ultros_site.routes.admin.users.demote import DemoteUserRoute
from ultros_site.routes.admin.users.disable_mfa import DisableUserMFARoute
from ultros_site.routes.admin.users.promote import PromoteUserRoute
from ultros_site.routes.admin.users.verify import VerifyUserRoute

__author__ = "Gareth Coles"
__all__ = ["DeleteUserRoute", "DemoteUserRoute", "DisableUserMFARoute", "PromoteUserRoute", "VerifyUserRoute"]
