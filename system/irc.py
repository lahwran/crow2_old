
"""
Object-oriented representation of irc.
"""

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from util.events import hook, Event

hook.create("privmsg", system=True)
hook.create("joined", system=True)
hook.create("left", system=True)
hook.create("noticed", system=True)

class Connection(irc.IRCClient):
    nickname = "crow2"

    def privmsg(self, user, channel, messages):
        hook.privmsg.fire(Event({"user": user, "channel": channel, "msg": messages}))

    def signedOn(self):
        self.join("##crow2")

    def ctcpQuery_VERSION(self, user, channel, data):
        if data is not None:
            self.quirkyMessage("Why did %s send '%s' with a VERSION query?"
                               % (user, data))

        if self.versionName:
            nick = string.split(user,"!")[0]
            self.ctcpMakeReply(nick, [('VERSION', '%s:%s:%s' %
                                       (self.versionName,
                                        self.versionNum or '',
                                        self.versionEnv or ''))])


class Channel(object):
    def __init__(self, name):
        self.name = name

class User(object):
    def __init__(self, name):
        self.name = name

