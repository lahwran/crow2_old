import sys
import time

import pytest

import crow2.plugin


ids = ("1", "B", "Z")

def create(path):
    f = path.open("w")
    f.write("")
    f.close()

def test_listpackage(tmpdir, monkeypatch):
    packagename = "test_listpackage_package"
    packagepath = tmpdir.join(packagename)
    children = set("child" + id for id in ids)

    packagepath.mkdir()
    create(packagepath.join("__init__.py"))
    for child in children:
        create(packagepath.join(child+".py"))

    getmodulename = lambda parent, name: name.partition(".")[0]
    monkeypatch.setattr(crow2.plugin, "getmodulename", getmodulename)
    monkeypatch.syspath_prepend(tmpdir)

    result = crow2.plugin.listpackage(packagename)

    del sys.modules[packagename]
    assert result == children

def test_getmodulename(tmpdir, monkeypatch):
    packagename = "test_getmodulename_package"
    packagepath = tmpdir.join(packagename)
    children = set(("child" + id, suffix) for suffix in crow2.plugin.suffixes
                                  for id in ids)
    subpackages = set(("pkg%d" % num, suffix) for num, suffix in enumerate(crow2.plugin.suffixes))
    emptydirs = set("emptydir" + id for id in ids)

    packagepath.mkdir()
    create(packagepath.join("__init__.py"))
    for name, suffix in children:
        create(packagepath.join(name + suffix))
    for subpackage, suffix in subpackages:
        subpackagepath = packagepath.join(subpackage)
        subpackagepath.mkdir()
        create(subpackagepath.join("__init__"+suffix))
    for emptydir in emptydirs:
        packagepath.join(emptydir).mkdir()

    for name, suffix in children:
        filename = name+suffix
        result = crow2.plugin.getmodulename(str(packagepath), filename)
        assert result == name
    for name, suffix in subpackages:
        result = crow2.plugin.getmodulename(str(packagepath), name)
        assert result == name
    for name in emptydirs:
        result = crow2.plugin.getmodulename(str(packagepath), name)
        assert result == None

def test_moduleloader():
    moduleloader = crow2.plugin.ModuleLoader("filename")


class TestPackageLoader(object):
    def test_repr(self, tmpdir):
        packagename = "test_packageloader_repr_package"
        packagepath = tmpdir.join(packagename)
        packagepath.mkdir()
        create(packagepath.join("__init__.py"))

        name = "packageloader_name_here"
        instance = crow2.plugin.PackageLoader(packagename, name)

        repred = repr(instance)
        assert packagename in repred

        stred = str(instance)
        assert packagename in stred
        assert name in stred

    def stub(self, path, name, reloaded):
        f = path.open("w")
        f.write("myname = %r\n" % name)
        f.write("reloaded = %r\n" % reloaded)
        f.close()

    def test_loader(self, tmpdir, monkeypatch):
        packagename = "test_packageloader_loader_package"
        packagepath = tmpdir.join(packagename)
        children = set("child" + id for id in ids)
        subpackage = "subpackage"
        emptydirs = set("emptydir" + id for id in ids)
        names = set((subpackage,)) | children

        packagepath.mkdir()
        create(packagepath.join("__init__.py"))
        for name in children:
            self.stub(packagepath.join(name + ".py"), name, False)
        subpackagepath = packagepath.join(subpackage)
        subpackagepath.mkdir()
        self.stub(subpackagepath.join("__init__.py"), subpackage, False)
        for emptydir in emptydirs:
            packagepath.join(emptydir).mkdir()

        monkeypatch.syspath_prepend(tmpdir)

        name = "packageloader_name_here"
        instance = crow2.plugin.PackageLoader(packagename, name)

        with pytest.raises(crow2.plugin.NotLoadedError):
            instance.unload()

        sysmodules = dict(sys.modules)

        instance.load()

        assert len(instance.plugins) == len(names)
        assert all([not plugin.reloaded for plugin in instance.plugins])
        assert all([plugin.myname in names for plugin in instance.plugins])

        with pytest.raises(crow2.plugin.AlreadyLoadedError):
            instance.load()

        instance.unload()

        assert sys.modules == sysmodules
        sysmodules = None

        for name in children:
            self.stub(packagepath.join(name + ".py"), name, True)
        self.stub(subpackagepath.join("__init__.py"), subpackage, True)

        instance.load()

        assert len(instance.plugins) == len(names)
        assert all([plugin.reloaded for plugin in instance.plugins])
        assert all([plugin.myname in names for plugin in instance.plugins])

        instance.unload()




