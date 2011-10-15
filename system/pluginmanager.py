
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
                        pass # TODO FIXME LOGGING VERY IMPORTANT
                        processed.add(submodule)
                    else:
                        pass # ignore it
                except Exception as e:
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



core = PluginManager("core")
plugins = PluginManager("plugins")


def loadall():
    events.hook.create("loaded", caller = lambda reg, e: reg.func())
    core.load()
    plugins.load()
    events.hook.loaded.fire(None)


def unloadall():
    core.unload()
    plugins.unload()
    events.hook._reset()
