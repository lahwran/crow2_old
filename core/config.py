
from twisted.internet import reactor

import os

import json

extensions = {"json": json}

try:
    import yaml
    extensions.update({"yaml": yaml, "yml": yaml})
except ImportError:
    pass


from util import hook
from system import irc


def stopstartup(event):
    """
    prevent startup if the config is missing
    """
    event.cancel()


@hook.startup
def loadconfig(event):
    bot = event.bot

    for ext, loader in extensions.items():
        try:
            reader = open("config.%s" % ext)
        except IOError as e:
            if e.errno == 2:
                continue
            else:
                raise

        print "loading from %s" % ext
        config = loader.load(reader)
        break
    else:
        # no config file, do something about it
        print "Config file not found! plz 2 make one kthx"
        hook._run(stopstartup)
        return

    servers = config["servers"]
    for name, info in servers.items():
        bot.servers[name] = irc.Server(**info)
        bot.servers[name].connect()

@hook.connect
def joinchans(event):
    for channel in event.server.config["channels"]:
        event.conn.join(channel)