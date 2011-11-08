

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

hook.command.fire("command")

events must be prepared in the hook object, like this:

class PrivmsgEvent(Event):
    '''
    Your docstring here
    '''

class CommandEvent(Event):
    '''
    Your docstring here
    '''

    def __init__(self, commandname):
        self.commandname = commandname

    @classmethod
    def _makeregistration(self, func, *args, **keywords):
        #alter keywords as fit
        return super(CommandEvent, self)._makeregistration(self, func, *args, **keywords)

"""

try:
    from crow2 import logger
except ImportError:
    print "Could not import logger from crow2, will not log exceptions in event handlers!"
import inspect


from util import misc

Order = misc.Enum("Order",
                  "earliest", "early_ignorecancelled", "early", 
                  "default_ignorecancelled", "default", "late_ignorecancelled", "late",
                  "latest_ignorecancelled", "latest", "monitor")

__all__ = ["main_hooks", "Hooks", "HandlerLists", "Order",
            "EventMissingException", "Event", "Registration"]


class Hooks(object):

    def __init__(self):
        self._events = {}
        self._systemevents = {}

    # make dict keys accessible as attributes
    def __getattr__(self, key):
        return self._getevent(key)

    def _reset(self):
        self._events = {}

    def _getevent(self, key):
        if key in self._systemevents:
            return self._systemevents[key]
        elif key in self._events:
            return self._events[key]
        else:
            raise EventMissingError(key)

    def _event_exists(self, key):
        try:
            self._getevent(key)
            return True
        except EventMissingError:
            return False

    def _create(self, name, cls, system=False):
        if self._event_exists(name):
            raise Exception("event already has been created: "+name+" (attempted class: %s)" % repr(cls))
        if system:
            self._systemevents[name] = HandlerList(cls)
        else:
            self._events[name] = HandlerList(cls)
    
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
main_hooks = Hooks()


class EventMetaclass(type):
    """
    Metaclass used to prepare an event class with a hook slot
    shouldn't be a metaclass, probably - perhaps a class decorator
    """
    def __init__(cls, name, bases, classdict):
        type.__init__(cls, name, bases, classdict)
        if classdict.get("_register", True):
            hooks = classdict.get("_hooks", main_hooks)

            defaultname = name.lower().replace("event", "")
            hookname = classdict.get("hookname", defaultname)

            system = classdict.get("_system", False)
            hooks._create(hookname, cls, system)


class Event(object):
    """
    Event superclass
    """
    __metaclass__ = EventMetaclass
    _register = False

    def _caller(self, registration):
        """
        used to modify the call of the handler. most events can leave this alone
        """
        registration.func(self)

    def _filter(self, registration):
        """
        Filters are a succinct way to filter when the handler is called. they should check values in the
        registration and return false if the registration does not match the call.
        """
        for key in registration.keywords:
            if key not in self.__dict__:
                return False
            if registration.keywords[key] != event.__dict__[key]:
                return False
        return True

    @classmethod
    def _makeregistration(self, func, *args, **keywords):
        """
        create an object to be used as a registration.
        this object must have a position attribute containing an element of the Order enum.
        """
        return Registration(func, args, keywords)


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


class CancellableEvent(Event):
    """
    A cancellable event.
    """
    _register = False
    cancelled = False

    def cancel(self):
        self.cancelled = True

    @classmethod
    def iscancellable(cls, position):
        return position.index % 2 == 0

    def _filter(self, registration):
        if self.cancelled and self.iscancellable(registration.position):
            return False
        return super(CancellableEvent, self)._filter(registration)

class HandlerList(object):

    def __init__(self, eventclass):
        self._registrations = {}
        for position in Order.lookup:
            self._registrations[position] = []
        self._eventclass = eventclass

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
        registration = self._eventclass._makeregistration(thefunc, *args, **keywords)
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

    def fire(self, *args, **keywords):
        """
        Fire an event with the provided arguments. Arguments are passed to the __init__ of the
        bound event class that was used to create this handler list, and the created object is returned
        after calling handlers.
        """
        try:
            event = self._eventclass(*args, **keywords)
        except TypeError as e:
            if "object.__new__()" in e.message:
                raise TypeError("%s - did you call your event constructor with incorrect parameters?" % e.message)
            else:
                raise
        self._call(event)
        return event

    def _call(self, event):
        "actually fire an event. does not create the event for you"
        for position in Order.lookup:
            for registration in self._registrations[position]:
                if not event._filter(registration):
                    continue
                event._caller(registration)
                # needs exception handling