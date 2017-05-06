# coding=utf-8
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    email = Column(String)
    email_verified = Column(Boolean, default=False)

    sessions = relationship("Session", back_populates="user")

    def __repr__(self):
        return "<User(id={}, username={}, email={}, verified={}, sessions={})>".format(
            self.id, self.username, self.email, self.email_verified, len(self.sessions)
        )
