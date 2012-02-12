import inspect
import functools

def paramdecorator(decorator_func):
    if inspect.getargspec(decorator_func).args[0] == "self":
        arg_func = 1
    else:
        arg_func = 0
    @functools.wraps(decorator_func)
    def meta_decorated(*args, **keywords):
        if len(args) == arg_func+1 and inspect.isfunction(args[arg_func]) and len(keywords) == 0:
            return decorator_func(*args)
        else:
            @functools.wraps(decorator_func)
            def decorator_return(func):
                newargs = list(args)
                newargs.insert(arg_func, func)
                return decorator_func(*newargs, **keywords)
            return decorator_return
    return meta_decorated

class Registration(object):
    pass

class Hook(object):
    def __call__(self, func, *args, **keywords):
        pass
