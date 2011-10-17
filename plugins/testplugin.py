# test plugin 1

from util import hook

#@hook.load
#def loaded(asdf):
#    print "whee I was loaded"

@hook.connect
def onconnect(event):
    event.connection.join("##crow2")

@hook.privmsg
def privmsg(event):
    print "{channel} <{user}> {msg}".format(**event)
