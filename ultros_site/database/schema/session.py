# coding=utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class Session(DeclarativeBase):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="children")
    token = Column(String(length=32), unique=True)
    expires = Column(DateTime)
    awaiting_mfa = Column(Boolean)

    def __repr__(self):
        return "<Session(id={}, user={}, expires={})>".format(
            self.id, self.user.username, self.expires
        )
