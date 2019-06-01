import importlib, sys

def import_mod(folder, name, package=None) :
    opath = sys.path
    sys.path.append(folder)
    m = importlib.import_module(name, package)
    sys.path = opath
    return m
