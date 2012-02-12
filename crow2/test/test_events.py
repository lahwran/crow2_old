import crow2.events
import pytest

def test_paramdecorator_simple():
    runs = []
    @crow2.events.paramdecorator
    def simple(func):
        runs.append(func)
        return func

    @simple
    def afunc():
        pass
    assert runs[-1] is afunc
    @simple()
    def afunc2():
        pass
    assert runs[-1] is afunc2
    with pytest.raises(TypeError):
        @simple("somearg")
        def afunc3():
            pass

def test_paramdecorator_requiredarg():
    lastrun = []
    @crow2.events.paramdecorator
    def decorator(func, requiredarg):
        del lastrun[:]
        lastrun.extend((func, requiredarg))
        return func

    with pytest.raises(TypeError):
        @decorator
        def afunc():
            pass

    somearg = object()
    @decorator(somearg)
    def afunc2():
        pass
    assert lastrun[0] is afunc2
    assert lastrun[1] is somearg

    somearg = object()
    @decorator(requiredarg=somearg)
    def afunc3():
        pass
    assert lastrun[0] is afunc3
    assert lastrun[1] is somearg


def test_paramdecorator_optionalarg():
    lastrun = []
    class Derp(object):
        def __init__(self, lastrun):
            self.lastrun=lastrun
        @crow2.events.paramdecorator
        def decorator(self, func, optionalarg1=None, optionalarg2=None):
            del self.lastrun[:]
            self.lastrun.extend((func, optionalarg1, optionalarg2))
            return func

    decorator = Derp(lastrun).decorator

    @decorator
    def afunc():
        pass
    assert lastrun[0] is afunc
    assert lastrun[1] is None
    assert lastrun[2] is None

    @decorator()
    def afunc():
        pass
    assert lastrun[0] is afunc
    assert lastrun[1] is None
    assert lastrun[2] is None

    somearg = object()
    @decorator(optionalarg1=somearg)
    def afunc():
        pass
    assert lastrun[0] is afunc
    assert lastrun[1] is somearg
    assert lastrun[2] is None

    somearg = object()
    with pytest.raises(TypeError):
        @decorator(derp=somearg)
        def afunc3():
            pass

def test_paramdecorator_quirks():
    lastrun = []
    @crow2.events.paramdecorator
    def decorator(func, func2):
        del lastrun[:]
        lastrun.extend((func, func2))
        return func() + func2()

    def func2():
        return "func2"

    with pytest.raises(TypeError):
        @decorator(func2)
        def func():
            return "func" #pragma: no cover

    @decorator(func2=func2)
    def func():
        return "func"
    assert func == "funcfunc2"
    assert lastrun[1] is func2
