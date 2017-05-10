# coding=utf-8
from falcon import HTTPForbidden
from sqlalchemy import func

from ultros_site.base_route import BaseRoute
from ultros_site.database.schema.user import User

__author__ = "Gareth Coles"


class UsersRoute(BaseRoute):
    route = "/admin/users"

    def on_get(self, req, resp):
        user = req.context["user"]

        if user and user.admin:
            page = req.get_param_as_int("page") or 1
            first_index = (page - 1) * 10
            last_index = page * 10

            db_session = req.context["db_session"]
            users = db_session.query(User).order_by(User.id)[first_index:last_index]
            count = db_session.query(func.count(User.id)).scalar()
            pages = int(count / 10)

            if count % 10:
                pages += 1
            if pages < 1:
                pages = 1

            self.render_template(
                req, resp, "admin/users.html",
                page=page,
                pages=pages,
                users=users,
                immune_user=self.manager.database.config["admin_username"]
            )
        else:
            raise HTTPForbidden()
