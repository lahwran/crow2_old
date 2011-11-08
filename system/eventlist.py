
from util import Event


class ConnectEvent(Event):
    """
    Fired when a connection to an IRC server is established.
    """
    _system = True

    def __init__(self, conn):
        self.conn = conn
        self.server = conn.server


class ChatEvent(Event):
    """
    Fired when a PRIVMSG message is receieved from the irc server
    """
    _system = True

    def __init__(self, user, channel, message):
        self.user = user
        self.channel = channel
        self.message = message

class StartupEvent(Event):
    """
    Fired when the system is starting up
    """
    _system = True

    def __init__(self, bot):
        self.bot = bot


class ShutdownEvent(Event):
    """
    Fired when the system is shutting down
    """
    _system = True

    def __init__(self, bot):
        self.bot = bot