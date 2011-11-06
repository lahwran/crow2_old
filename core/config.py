from util import hook

from twisted.internet import reactor
from system import irc

import json

try:
    import yaml
except ImportError:
    yaml = None

extensions = {"json": json, "yaml": yaml, "yml": yaml}

@hook.startup
def createconnections(event):
    event.bot.servers["test"] = irc.Server("localhost", 6667, "crow2", "crow2", "crow2", None, [])
    event.bot.servers["test"].connect()