# coding=utf-8
from sqlalchemy import Column, Integer, String
from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(id={}, username={}, email={})>".format(
            self.id, self.username, self.email
        )
