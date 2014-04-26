__author__ = 'Gareth Coles'

import datetime

from sqlalchemy import Integer, Sequence, Column, String, Boolean, DateTime, \
    PickleType
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Bot(base):
    """
    Bot represents a row in the "bots" table. Each row represents an Ultros bot
    and its metrics.

    Columns:
    * id - Unique row ID
    * uuid - UUID used to identify the bot
    * enabled - Whether metrics are enabled for the bot
    * packages - List of installed package dicts
    * plugins - List of installed plugin dicts
    * first_seen - Date the bot was first seen
    * last_seen - Date the bot was last seen
    """

    __tablename__ = "bots"
    id = Column(Integer, Sequence('bots_id_seq'), primary_key=True)
    uuid = Column(String(36))
    enabled = Column(Boolean())
    packages = Column(String(256))
    plugins = Column(String(256))
    protocols = Column(String(256))
    first_seen = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))

    def __init__(self, uuid, enabled=True, packages=None, plugins=None,
                 protocols=None, first_seen=None, last_seen=None):

        if packages is None:
            packages = "||"
        if plugins is None:
            plugins = "||"
        if protocols is None:
            protocols = "||"
        if first_seen is None:
            first_seen = datetime.datetime.now()
        if last_seen is None:
            last_seen = datetime.datetime.now()

        self.uuid = uuid
        self.enabled = enabled
        self.packages = packages
        self.plugins = plugins
        self.protocols = protocols
        self.first_seen = first_seen
        self.last_seen = last_seen

    def to_dict(self):
        """
        Convert this Bot into a dict.
        """
        return {
            "enabled": self.enabled,
            "packages": self.packages,
            "plugins": self.plugins,
            "first_seen": str(self.first_seen),
            "last_seen": str(self.last_seen)
        }

    def __repr__(self):
        return "<Bot(uuid=%s, enabled=%s, %d packages, %d plugins, " \
               "first_seen=%s, last_seen=%s)>" % (
                   self.uuid, self.enabled, len(self.packages),
                   len(self.plugins), self.first_seen, self.last_seen
               )


class Obj(base):
    """
    Obj represents lists of things we track in bots. Each Obj has a type and
    name, and (right now) stores all protocols, plugins and packages
    that people have installed.

    Columns:
    * id - Unique row ID
    * what - String, type of Obj
    * who - String, name of Obj
    """

    __tablename__ = "objs"
    id = Column(Integer, Sequence('objs_id_seq'), primary_key=True)
    what = Column(String(64))
    who = Column(String(128))

    def __init__(self, what, who):
        self.what = what
        self.who = who

    def to_dict(self):
        """
        Convert this Obj into a dict.
        """
        return {
            "type": self.type,
            "name": self.name
        }

    def __repr__(self):
        return "<Obj(what=%s, who=%s)>" % (
            self.what, self.who
        )


class User(base):
    """
    User represents a username and auth token for a GitHub login.

    Columns:
    * id - Unique row ID
    * username - String, username of the user
    * token - String, authorization token for use with GitHub calls
    * data_* - String, Pickled dict of various pieces of info
    """

    __tablename__ = "users"
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    username = Column(String(64))
    token = Column(String(128))
    data_user = Column(PickleType())
    data_user_repos = Column(PickleType())
    data_orgs = Column(PickleType())
    data_orgs_repos = Column(PickleType())

    def __init__(self, username, token,
                 data_user, data_user_repos, data_orgs, data_orgs_repos):
        self.username = username
        self.token = token
        self.data_user = data_user
        self.data_user_repos = data_user_repos
        self.data_orgs = data_orgs
        self.data_orgs_repos = data_orgs_repos

    def to_dict(self):
        """
        Convert this Obj into a dict.
        """
        return {
            "username": self.username,
            "token": self.token
        }

    def __repr__(self):
        return "<Obj(username=%s, token=%s)>" % (
            self.username, self.token
        )


Bot.base = base
Obj.base = base
User.base = base
