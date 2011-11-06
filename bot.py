#!/usr/bin/python

from util import prepare

prepare.prepare()


def main():
    try:
        from twisted.internet import reactor
    except ImportError:
        print "crow2 depends on twisted!"
        return

    try:
        import exocet
    except ImportError:
        print "Exocet not found, downloading"
        download_exocet()
    from system import eventlist, pluginmanager, irc
    from util import hook, Event


    bot = irc.Client()

    pluginmanager.loadall()

    hook.startup.fire(bot)

    try:
        reactor.run()
    finally:
        hook.shutdown.fire(bot)
        pluginmanager.unloadall()

if __name__ == "__main__":
    main()



#this code will extract a tarball, usefull for autodownloading exocet if it's missing

#import os, sys, tarfile

#try:
    #tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    #for item in tar:
        #tar.extract(item)