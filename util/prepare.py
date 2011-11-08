"""
Contains utilities to prepare the environment for crow2
"""

import logging

exocet_url = "http://launchpad.net/exocet/trunk/0.5/+download/Exocet-0.5.tar.gz"

def prepare_exocet():
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

def prepare_twisted():
    print "gimme twisted :<"

def prepare():
    try:
        import exocet
    except ImportError:
        prepare_exocet()

    try:
        import twisted
    except ImportError:
        prepare_twisted()
        raise