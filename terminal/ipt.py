import importlib

def ipf(name):
    try:
        return importlib.import_module(str(name).replace("/", ".").replace("\\", "."))
    except ImportError as e:
        pass
