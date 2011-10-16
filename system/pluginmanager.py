
import exocet
from util import events


class PluginManager(object):
    def __init__(self, module):
        self.module = module
    
    def reload(self):
        self.unload()
        self.load()
    
    def load(self):
        "direct translation of bukkit equivalent"
        submodules = set(exocet.getModule(self.module).iterModules())
        processed = set()
        self.plugins = []

        allfailed = False
        finalpass = False

        # TODO FIXME should map all non-loaded plugins away so they're not importable
        # and should map loaded plugins so they're not loaded twice
        mapper = exocet.pep302Mapper

        while (not allfailed) or finalpass:
            allfailed = True

            for submodule in submodules - processed:
                plugin = None
                try:
                    plugin = exocet.load(submodule, mapper)
                except (ImportError, events.EventMissingError) as e:
                    if finalpass:
                        print e
                        pass # TODO FIXME LOGGING VERY IMPORTANT
                        processed.add(submodule)
                    else:
                        pass # ignore it
                except Exception as e:
                    print e
                    pass # TODO FIXME LOGGING VERY IMPORTANT
                    processed.add(submodule)

                if plugin:
                    self.plugins.append(plugin)
                    allfailed = False
                    finalpass = False
                    processed.add(submodule)

            if finalpass:
                break
            elif allfailed:
                finalpass = True

    def unload(self):
        del self.plugins

class Plugin(object):
    def __init__(self):
        pass #stuff happens here

core = PluginManager("core")
plugins = PluginManager("plugins")

def loadall():
    core.load()
    plugins.load()
    #TODO FIXME need to give plugins access to the bot and such here
    events.hook.load.fire(None)


def unloadall():
    #TODO FIXME does this need to have stuff
    events.hook.unload.fire(None)
    core.unload()
    plugins.unload()
    events.hook._reset()

events.hook.create("load", system = True)
events.hook.create("unload", system = True)