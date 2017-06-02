# coding=utf-8
from sqlalchemy import Column, Integer, String

from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class Setting(DeclarativeBase):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)

    def __repr__(self):
        return "<{}(key={}, value={})>".format(
            self.__class__.__name__,
            self.key, self.value
        )
