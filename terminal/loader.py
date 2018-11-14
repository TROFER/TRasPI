import log
import importlib

modules = {}

def load(name):
    name = str(name).replace("/", ".").replace("\\", ".")
    try:
        modules[name.split(".")[-1]] = importlib.import_module(name)
    except ImportError as e:
        log.err(e)

def reload(name):
    try:
        return importlib.reload(name)
    except ImportError as e:
        log.err(e)
