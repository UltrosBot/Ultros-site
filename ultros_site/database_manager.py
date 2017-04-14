# coding=utf-8
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yaml import load

__author__ = "Gareth Coles"
log = logging.getLogger("Database")


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.make_session = None

        self.config = load(open("config.yml", "r"))

    def create_engine(self):
        log.info("Creating database engine...")
        url = self.config["database_url"]

        self.engine = create_engine(url, echo=self.config.get("debug", False))
        self.make_session = sessionmaker(self.engine)

    def create_session(self):
        return self.make_session()
