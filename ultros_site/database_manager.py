# coding=utf-8
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ruamel.yaml as yaml

__author__ = "Gareth Coles"
log = logging.getLogger("Database")


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.make_session = None

        with open("config.yml", "r") as fh:
            self.config = yaml.safe_load(fh)

    def create_engine(self):
        log.info("Creating database engine...")
        url = self.config["database_url"]

        self.engine = create_engine(url, echo=self.config.get("debug", False))
        self.make_session = sessionmaker(self.engine)

    def create_session(self):
        return self.make_session()
