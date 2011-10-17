

"""
examples of registering an event handler:

@hook.privmsg
def someone_talked(event):
    print event.msg

@hook.privmsg(chan="#risucraft")
def risucraft_spammed(event):
    print "QUICK +m RISUCRAFT! SOMEONE IS SPAMMING IT!"

@hook.sieve(position = Order.early)
def ignore(event):
    if "nick" in event and event.nick in ignorelist:
        event.cancel()

@hook.sending_chat
def censor(event):
    for i in censors:
        event.msg.replace(i, "[CENSORED]")

@hook.command
def google(event):
    googlesearch.google(event.arg)

examples of calling an event:

event = whatever
hook.command.handlers(event)

events must be prepared in the hook object, like this:

hook.create("privmsg")

def command_filter(func, name=None, *args, **keywords):
    if not name:
        name = func.func_name
    def filter(event):
        return event.command == name
    return filter

hook.create("command", command_filter)

"""

try:
    from crow2 import logger
except ImportError:
    print "Could not import logger from crow2, will not log exceptions in event handlers!"
import inspect
import UserDict

__all__ = ["hook", "Hooks", "HandlerLists", "Order",
            "EventMissingException", "defaultcaller",
            "defaultfilter", "Event", "Registration", "__can_register_system__"]

def defaultcaller(registration, event):
    registration.func(event)

def defaultfilter(registration, event):
    for key in registration.keywords:
        if key not in event:
            return False
        if registration.keywords[key] != event[key]:
            return False
    return True

class Registration(object):
    "registration data holder, should probably use a namedtuple for this"
    def __init__(self, thefunc, args, keywords):
        self.position = Order.default
        if "position" in keywords:
            position = keywords["position"]
            del keywords["position"]
        self.args = args
        self.keywords = keywords
        self.func = thefunc


class Hooks(object):

    def __init__(self):
        self._events = {}

    # make dict keys accessible as attributes
    def __getattr__(self, key):
        if key in self._events:
            return self._events[key]
        else:
            raise EventMissingError(key)

    def _reset(self):
        for item in self._events.items():
            if not item[1]._system:
                del self._events[item[0]]

    def create(self, name, caller = defaultcaller, makereg = Registration, *filters, **keywords):
        if name in self._events:
            raise Exception("event already has been created: "+name)
        deffilter = keywords["deffilter"] if "deffilter" in keywords else True
        system = keywords["system"] if "system" in keywords else False
        self._events[name] = HandlerLists(caller, filters, deffilter, makereg, system)
    
    def _delete(self, name):
        if name not in self._events:
            raise EventMissingError(name)
        del self._events[name]

# this name seems too java-ey
class EventMissingError(Exception):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Event %r Missing" % self.name
    def __repr__(self):
        return "EventMissingError(%r)" % self.name

# this object is what plugins will have available
hook = Hooks()


class Event(dict):
    "utility class intended for use as event objects"
    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return self.__getitem__(key)
    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self.__setitem__(key, value)

class CancellableEvent(Event):
    def __init__(self, *args, **keywords):
        Event.__init__(self, *args, **keywords)
        self.cancelled = False
    def cancel(self):
        self.cancelled = True

class HandlerLists(object):

    def __init__(self, caller = defaultcaller, filters = (), deffilter = True, makereg = Registration, system=False):
        self._registrations = {}
        for position in Order.lookup:
            self._registrations[position] = []
        if deffilter:
            filters = (defaultfilter, ) + filters
        self._filters = filters
        self._caller = caller
        self._makeregistration = makereg
        self._system = system

    def __call__(self, *args, **keywords):
        "this is called as the hook.* decorators"
        
        # first check if we're being called as @decorator or as @decorator(...)
        if len(args) == 1 and len(keywords) == 0 and inspect.isfunction(args[0]):
            # called as @decorator - single function argument
            # ie, args[0] is the function to register, and no arguments have
            # been provided
            self.register(args[0])
            return args[0]
        else:
            # called as @decorator(args) - return a handler
            # ie, we're being called as inst()(func)
            def decorate(func):
                self.register(func, args, keywords)
            return decorate

    def register(self, thefunc, args=(), keywords={}):
        "register a handler"
        registration = Registration(thefunc, args, keywords)
        self._registrations[registration.position].append(registration)

    def unregister(self, thefunc, args=(), keywords={}):
        "unregister a handler"
        positions = Order.lookup
        if "position" in keywords:
            positions = (keywords["position"],)
            del keywords["position"]
        for position in positions:
            for registration in self.registrations[position]:
                if thefunc != registration.func or args != registration.args:
                    continue
                if registration.keywords != keywords:
                    continue
                self.registrations[position].remove(registration)
        

    def _checkfilters(self, registration, event):
        for filter in self._filters:
            if not filter(registration, event):
                return False
        return True

    def fire(self, event):
        "actually fire an event"
        for position in Order.lookup:
            for registration in self._registrations[position]:
                if not self._checkfilters(registration, event):
                    continue
                #try:
                self._caller(registration, event)
                #except Exception as e:
                #    logger.exception(e)
                

__can_create_order__ = True

class Order(object):

    lookup = ["earliest", "early_ignorecancelled", "early", 
      "default_ignorecancelled", "default", "late_ignorecancelled", "late",
      "latest_ignorecancelled", "latest", "monitor"]

    def __init__(self, index, name):
        if not __can_create_order__:
            raise Exception("Order initialization is already complete, use Order.whatever (see dir(Order))")
        self.index = index
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Order."+self.name



for index in range(len(Order.lookup)):
    name = Order.lookup[index]
    Order.lookup[index] = Order(index, name)
    setattr(Order, name, Order.lookup[index])
del name

__can_create_order__ = False


