from util import hook

from twisted.internet import reactor
from system import irc

from core import config

@hook.load
def createconnections(event):
    reactor.connectTCP("irc.esper.net", 6667, irc.Connector("crow2"))