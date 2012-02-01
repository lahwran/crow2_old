import sys

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

def test_packageloader(tmpdir):
    packagename = "test_packageloader_package"
    packagepath = tmpdir.join(packagename)
    children = set("child" + id for id in ids)

    
    packagepath.mkdir()
    create(packagepath.join("__init__.py"))
    for name, suffix in children:
        create(packagepath.join(name + suffix))

    monkeypatch.syspath_prepend(tmpdir)



