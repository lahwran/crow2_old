#!/usr/bin/python


exocet_url = "http://launchpad.net/exocet/trunk/0.5/+download/Exocet-0.5.tar.gz"

def download_exocet():
    import urllib
    import tarfile
    import os

    temploc = "exocet_temp.tar.gz"

    print "Downloading %s" % exocet_url
    urllib.urlretrieve(exocet_url, temploc)
    print "Downloaded to %s" % temploc, "extracting"
    tar = tarfile.open(temploc, 'r:gz')
    for item in tar:
        if item.name.startswith("Exocet-0.5/exocet"):
            item.name = item.name.replace("Exocet-0.5/", "")
        else:
            continue
        tar.extract(item)
    print "Extracted, deleting %s" % temploc
    os.unlink(temploc)
    print "Done downloading exocet"

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

    hook.startup.fire(Event(bot = bot))

    try:
        reactor.run()
    finally:
        hook.shutdown.fire(Event(bot = bot))
        pluginmanager.unloadall()

if __name__ == "__main__":
    main()



#this code will extract a tarball, usefull for autodownloading exocet if it's missing

#import os, sys, tarfile

#try:
    #tar = tarfile.open(sys.argv[1] + '.tar.gz', 'r:gz')
    #for item in tar:
        #tar.extract(item)