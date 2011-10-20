class TestMC(type):
    def __new__(cls, classname, bases, classdict):
        print cls
        print classname
        print bases
        print classdict
        print
        return type.__new__(cls, classname, bases, classdict)

class Event(object):
    __metaclass__ = TestMC
    @classmethod
    def something(cls):
        print cls

class SomeEvent(Event):
    pass

class OtherEvent(Event):
    @classmethod
    def something(cls):
        print "happy time"

Event.something()
SomeEvent.something()
OtherEvent.something()