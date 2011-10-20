"""
A dropbox for uncategorized utility code that doesn't belong anywhere else.
"""

import warnings
import inspect
import functools

def deprecated(arg):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    info = ""
    def decorate(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn_explicit("Call to deprecated function %s%s." % (func.__name__, info),
                          category=DeprecationWarning,
                          filename=func.func_code.co_filename,
                          lineno=func.func_code.co_firstlineno + 1)
            return func(*args, **kwargs)
        return new_func
    if inspect.isfunction(arg):
        return decorate(func)
    else:
        info = ", "+arg
        return decorate

class EnumElement(object):

    def __init__(self, owner, index, name):
        self.index = index
        self.name = name
        self.owner = owner

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.owner.name + "." + self.name

class Enum(object):

    def __init__(self, enumname, *lookup):
        self.name = enumname
        lookup = list(lookup)
        self.lookup = lookup
        for index in range(len(lookup)):
            elementname = lookup[index]
            lookup[index] = EnumElement(enumname, index, elementname)
            setattr(self, elementname, lookup[index])

    def __repr__(self):
        return "Enum(%r)" % self.name