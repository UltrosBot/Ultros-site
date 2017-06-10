# coding=utf-8
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from ultros_site.database.common import DeclarativeBase

__author__ = "Gareth Coles"


class BackupCode(DeclarativeBase):
    __tablename__ = "backup_code"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="backup_codes")
    code = Column(String(length=32), unique=True)

    def __repr__(self):
        return "<{}(id={}, user={})>".format(
            self.__class__.__name__,
            self.id, self.user.username
        )
