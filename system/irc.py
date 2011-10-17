
"""
Object-oriented representation of irc.
"""

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.internet.protocol import ClientFactory

from util.events import hook, Event

hook.create("connect", system=True)
hook.create("privmsg", system=True)
hook.create("joined", system=True)
hook.create("left", system=True)
hook.create("noticed", system=True)


class Connector(ClientFactory):
    def __init__(self, nickname):
        self.nickname = nickname

    def startedConnecting(self, connector):
        pass
        #print 'Started to connect.'

    def buildProtocol(self, addr):
       # print 'Connected.'
        return Connection(self.nickname)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

class Connection(irc.IRCClient):

    def __init__(self, nickname):
        self.nickname = nickname


    def privmsg(self, user, channel, messages):
        hook.privmsg.fire(Event({"user": user, "channel": channel, "msg": messages}))

    def signedOn(self):
        hook.connect.fire(Event({"connection": self}))

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
    def __init__(self, connection, name):
        self.name = name

class User(object):
    def __init__(self, name):
        self.name = name

