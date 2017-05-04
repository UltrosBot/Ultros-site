# coding=utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    sessions = relationship("Session", back_populates="parent")

    def __repr__(self):
        return "<User(id={}, username={}, email={}, sessions={})>".format(
            self.id, self.username, self.email, len(self.sessions)
        )
