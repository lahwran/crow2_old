
"""
Object-oriented representation of irc.
"""

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.internet.protocol import ReconnectingClientFactory

from util.events import hook, Event
from util.misc import deprecated

class Client(object):
    "A class representing the bot or client, including all connections and config and such"
    def __init__(self):
        self.servers = {}

class Server(object):
    def __init__(self, address, port, nickname, username, realname, password, config):
        self.address = address
        self.port = port
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.password = password
        self.config = config

        self.connecting = False

        self._connection = None
        self._connfactory = None
        self._connector = None

    @property
    def isconnected(self):
        if self._connection == None:
            return False
        if self._connection.isconnected:
            return True

    @property
    def isready(self):
        if not self.isconnected:
            return False
        return self._connection.isready

    def connect(self):
        # need to make this check better, will probably cause errors 
        # once in a blue moon
        if self.isconnected or self.connecting:
            return
        
        self.connecting = True
        if self._connfactory == None:
            self._connfactory = ConnectionFactory(self)
        reactor.connectTCP(self.address, self.port, self._connfactory)

    def disconnect(self):
        if not self.isconnected and not self.connecting:
            return
        if not self._connector:
            return
        self._connfactory.stopTrying()
        self._connector.disconnect()
        self._connection = None
        self._connector = None
        self._connfactory = None
        self.connecting = False




#this really should be part of Server, not a separate class ...
class ConnectionFactory(ReconnectingClientFactory):
    def __init__(self, server):
        self.server = server

    def startedConnecting(self, connector):
        ReconnectingClientFactory.startedConnecting(self, connector)
        self.server._connector = connector

    def buildProtocol(self, addr):
        self.server._connection = Connection(self.server)
        self.resetDelay()
        return self.server._connection

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        self.server._connector = connector

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        self.server._connector = connector



class Connection(irc.IRCClient):

    def __init__(self, server):
        self.server = server
        self.nickname = server.nickname
        self.password = server.password
        self.realname = server.realname
        self.username = server.username
        self.isconnected = False
        self.isready = False

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.server.connecting = False
        self.isconnected = True
        self.isready = False
    
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.isconnected = False
        self.isready = False

    def privmsg(self, user, channel, msg):
        hook.privmsg.fire(Event(user=user, channel=channel, msg=msg))

    def signedOn(self):
        self.isready = True
        hook.connect.fire(Event({"connection": self}))

class Channel(object):
    def __init__(self, connection, name):
        self.name = name
    
    @deprecated("please use Channel.action()")
    def act(self, message):
        self.action(message)
    @deprecated("please use Channel.action()")
    def me(self, message):
        self.action(message)
    def action(self, message):
        print "doooop", message

class User(object):
    def __init__(self, name):
        self.name = name

