
from crow2 import hook

@hook.instantiate
class SomeClass(object):
    
    @hook.SOMEHOOK.method
    def somemethod(self):
        fdsa
    @hook.SOMEHOOK.method(params)
    def somemethod(self):
        asdf

@hook.SOMEHOOK
def somefunc():
    fdsa
@hook.SOMEHOOK(params)
def somefunc():
    asdf

@hook.category.OTHERHOOK
@
