#!/usr/bin/python

from system import eventlist, pluginmanager, irc
from twisted.internet import reactor
from util import hook, Event

bot = irc.Client()

pluginmanager.loadall()

hook.startup.fire(Event(bot = bot))

try:
    reactor.run()
finally:
    hook.shutdown.fire(Event(bot = bot))
    pluginmanager.unloadall()



#this code will extract a tarball, usefull for autodownloading exocet if it's missing

#import os, sys, tarfile

#try:
    #tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    #for item in tar:
        #tar.extract(item)