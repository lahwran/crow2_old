#!/usr/bin/python

from util import prepare

prepare.prepare()

from util.events import Order, CancellableEvent
from util import hook

class _Run(CancellableEvent):
    """
    A special event - a handler for this event should start the event loop
    intended for making plugins that run the reactor differently
    """

@hook._run(position=Order.latest)
def startreactor(event):
    from twisted.internet import reactor
    reactor.run()


def main():
    import exocet

    from system import eventlist, pluginmanager, irc

    bot = irc.Client()

    pluginmanager.loadall()

    try:
        hook.startup.fire(bot)
        hook._run.fire()
    finally:
        hook.shutdown.fire(bot)
        pluginmanager.unloadall()

if __name__ == "__main__":
    main()