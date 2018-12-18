import core.log
import importlib

log = core.log.name("Loader")
modules = {}

def load(name):
    name = str(name).replace("/", ".").replace("\\", ".")
    try:
        modules[name.split(".")[-1]] = importlib.import_module(name)
        return True
    except ImportError as e:
        log.err(e)
    except BaseException as e:
        log.err("Error loading module ({}): {}: {}".format(name, type(e).__name__, e))
    return False

def reload(name):
    try:
        module = modules[str(name)]
    except KeyError as e:
        log.err("No loaded module named "+str(e))
        return False
    try:
        importlib.reload(module)
        return True
    except ImportError as e:
        log.err(e)
    return False
