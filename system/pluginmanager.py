
import exocet
from util import hook, Event

from traceback import print_exc

from zope.interface import implements

class ModuleChecker(object):
    implements(exocet.IMapper)
    def __init__(self, parent, submodules):
        self.submodules = submodules
        self.parent = parent


    def lookup(self, name):
        try:
            if name.startswith(self.parent.module): #next three lines check if it belongs to us
                for submodule in self.submodules:
                    if name == submodule.name:
                        try:
                            return self.parent.getplugin(name)
                        except KeyError:
                            raise ImportError("plugin "+name+" not loaded")
            else:
                for manager in managers.values():
                    if manager == self.parent:
                        continue

                    if not manager.loaded and name.startswith(manager.module):
                        raise ImportError("attempting to import a module that belongs to an unloaded plugin loader")

                    try:
                        return manager.getplugin(name)
                    except KeyError:
                        pass #not an error, just doesn't belong to that loader

            # if the above code did not result in exiting
            # this method, we may safely load the module normally
            return exocet.pep302Mapper.lookup(name)
        except ImportError:
            raise
        except Exception as e:
            print e
            raise ImportError("error while importing: "+str(e))



    def contains(self, name):
        """
        @see L{IMapper.contains}
        """
        try:
            self.lookup(name)
            return True
        except ImportError:
            return False



class PluginManager(object):
    def __init__(self, module):
        self.module = module
        self._clear()

    def reload(self):
        self.unload()
        self.load()

    def getplugin(self, name):
        return self.plugmap[name]

    def _clear(self):
        self.plugins = []
        self.plugmap = {}
        self.loaded = False

    def load(self):
        "direct translation of bukkit equivalent"
        submodules = set(exocet.getModule(self.module).iterModules())
        processed = set()
        self._clear()

        allfailed = False
        finalpass = False

        # TODO FIXME should map all non-loaded plugins away so they're not importable
        # and should map loaded plugins so they're not loaded twice
        mapper = ModuleChecker(self, submodules)

        while (not allfailed) or finalpass:
            allfailed = True

            for submodule in submodules - processed:
                plugin = None
                try:
                    plugin = exocet.load(submodule, mapper)
                except ImportError as e:
                    if finalpass:
                        print_exc() # TODO FIXME LOGGING VERY IMPORTANT
                        processed.add(submodule)
                    else:
                        pass # ignore it
                except:
                    print_exc() # TODO FIXME LOGGING VERY IMPORTANT
                    processed.add(submodule)

                if plugin:
                    self.plugins.append(plugin)
                    self.plugmap[plugin.__name__] = plugin
                    allfailed = False
                    finalpass = False
                    processed.add(submodule)

            if finalpass:
                break
            elif allfailed:
                finalpass = True
        self.loaded = True

    def unload(self):
        self._clear()

class Plugin(object):
    def __init__(self):
        pass #stuff happens here

managers = {"core": PluginManager("core"), "plugins": PluginManager("plugins")}

def loadall():
    for manager in managers.values():
        manager.load()
    #TODO FIXME need to give plugins access to the bot and such here
    hook.load.fire()


def unloadall():
    #TODO FIXME does this need to have stuff
    hook.unload.fire()
    for manager in managers.values():
        manager.unload()
    hook._reset()

class LoadEvent(Event):
    """
    Fired just after plugins are loaded. First fire is before
    StartupEvent, but is also fired on subsequent reloads.
    """
    _system = True

class UnloadEvent(Event):
    """
    Fired just before plugins are unloaded. Last fire is just
    after ShutdownEvent, but can be fired before that from reloads.
    """
    _system = True