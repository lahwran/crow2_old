#!/usr/bin/python

import exocet

from system import pluginmanager, irc


from twisted.internet.protocol import ClientFactory

class Connector(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return irc.Connection()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

from twisted.internet import reactor
reactor.connectTCP("irc.esper.net", 6667, Connector())

pluginmanager.loadall()

reactor.run()





#this code will extract a tarball, usefull for autodownloading exocet if it's missing

#import os, sys, tarfile

#try:
    #tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    #for item in tar:
        #tar.extract(item)