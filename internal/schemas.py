__author__ = 'Gareth Coles'

import datetime

BOT = {
    "uuid": unicode,  # Bot UUID
    "enabled": bool,  # Whether metrics are enabled
    "packages": list,  # List of installed packages
    "plugins": list,  # List of enabled plugins
    "protocols": list,  # List of enabled protocol types
    "first_seen": datetime.datetime,  # Date the bot was first seen
    "last_seen": datetime.datetime  # Date the bot was last seen
}

OBJ = {
    "type": str,  # Type of object
    "name": unicode  # Name of object
}

USER = {
    "username": str,  # GitHub username
    "token": str,  # Auth token from GitHub
    "data_user": dict,  # User data
    "data_user_repos": dict,  # User repo data
    "data_orgs": dict,  # User organisations
    "data_orgs_repos": dict  # Repos for organisations
}

EXCEPTION = {
    "uuid": unicode,  # UUID of the user's exception
    "traceback": unicode,  # The exception traceback
    "type": unicode,  # The exception type
    "value": unicode,  # The exception value
    "date": datetime.datetime,  # When the exception was submitted
    "scope": dict  # Innermost frame local scope
}

schemas = {
    "bots": BOT,
    "objs": OBJ,
    "users": USER,
    "exceptions": EXCEPTION
}
