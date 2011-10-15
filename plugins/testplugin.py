# test plugin 1

from util import hook

@hook.loaded
def loaded():
    print "whee I was loaded"