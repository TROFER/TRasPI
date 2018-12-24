import core.log
import importlib
import os

log = core.log.name("Loader")
modules = {}

def load(name):
    name = str(name).replace("/", ".").replace("\\", ".")
    preprocess(name.replace(".", "/"))
    try:
        modules[name.split(".")[-1]] = importlib.import_module(name)
        return True
    except ImportError as e:
        log.err(e)
    except BaseException as e:
        log.err("Error loading module ({}): {}: {}".format(name, type(e).__name__, e))
    return False

def preprocess(name):
    modules = []
    with open(name, "r+") as file:
        length = 0
        for line in file:
            line = line.strip()
            if line[0] != "#":
                break
            elif "$PIP" in line:
                modules = line[line.index("$PIP")+4:].strip().replace(", ", ",").split(",")
                file.seek(length, 0)
                file.write(line.replace("$", " "))
                break
            length += len(line)+2
    pip(modules)

def pip(*modules):
    if modules:
        log.info("Pip Installing: {}".format(", ".join(modules)))
        for module in modules:
            os.system("python3 -m pip install {} -t dependencies/pip/".format(module))

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
