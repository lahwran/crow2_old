# test plugin 1

from util import hook

#@hook.load
#def loaded(asdf):
#    print "whee I was loaded"

#@hook.connect
#def onconnect(event):
#    event.conn.join("##crow2")

@hook.chat
def privmsg(event):
    print "{channel} <{user}> {message}".format(**event.__dict__)
