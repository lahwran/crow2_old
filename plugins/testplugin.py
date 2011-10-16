# test plugin 1

from util import hook

@hook.load
def loaded(asdf):
    print "whee I was loaded"

@hook.privmsg
def privmsg(event):
    print event
