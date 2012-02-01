import imp
import os
import sys

from twisted.python.reflect import namedModule

class AlreadyLoadedError(Exception):
    pass

class NotLoadedError(Exception):
    pass


class PackageLoader(object):
    """
    manages a plugin package - loads submodules as packages
    """
    def __init__(self, package, name=None):
        self.package = package
        self.loaded = False
        self.plugins = []
        self.name = name

    def load(self):
        if self.loaded:
            raise AlreadyLoadedError(self.package)
        self.plugins = []
        names = listpackage(repr(self))
        for name in names:
            plugin = namedModule(parent, name)
            self.plugins.append(plugin)
        self.loaded = True
        # that was easy

    def unload(self):
        if not self.loaded:
            raise NotLoadedError(repr(self))
        for name in sys.modules:
            if name.startswith(self.package+".") or name == self.package:
                del sys.modules[name]
        self.plugins = []
        self.loaded = False

        #unload from sys.modules, empty out our bowels

    def __repr__(self):
        return "<PackageLoader(%r)>" % self.package

    def __str__(self):
        return "Package %r: %s" % (self.package, self.name)

class ModuleLoader(object):
    def __init__(self, filename):
        pass

suffixes = set([info[0] for info in imp.get_suffixes()])
def getmodulename(parent, filename):
    for suffix in suffixes:
        if filename.endswith(suffix):
            return filename[:-len(suffix)] # remove ending
    else:
        fullpath = os.path.join(parent, filename)
        if os.path.isdir(fullpath):
            for suffix in suffixes:
                if os.path.exists(os.path.join(fullpath, "__init__"+suffix)):
                    return filename

def listpackage(name):
    parent = namedModule(name)
    results = set()
    for package_path in parent.__path__:
        files = os.listdir(package_path)

        for filename in files:
            modulename = getmodulename(package_path, filename)
            if not modulename or modulename == "__init__":
                continue
            print filename, modulename
            results.add(modulename)

    return results
