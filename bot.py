#!/usr/bin/python

from system import pluginmanager, irc
from twisted.internet import reactor

pluginmanager.loadall()
try:
    reactor.run()
finally:
    pluginmanager.unloadall()



#this code will extract a tarball, usefull for autodownloading exocet if it's missing

#import os, sys, tarfile

#try:
    #tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    #for item in tar:
        #tar.extract(item)