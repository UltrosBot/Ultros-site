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

EXCEPTION = {
    "uuid": unicode,  # UUID of the user's exception
    "traceback": unicode,  # The exception traceback
    "type": unicode,  # The exception type
    "value": unicode,  # The exception value
    "date": datetime.datetime,  # When the exception was submitted
    "scope": dict  # Innermost frame local scope
}

SYSTEM = {
    "uuid": unicode,
    "ram": float,  # Amount of RAM (in MB)
    "cpu": unicode,
    "os": unicode,
    "python": unicode
}

schemas = {
    "bots": BOT,
    "objs": OBJ,
    "exceptions": EXCEPTION,
    "systems": SYSTEM
}
