import sys
import importlib.util

from core.sys import PATH
from core.render.window import Window
import core.error

__all__ = ["window", "module"]

_loading_count = 0

def window(file: str, path: str=""):
    _module = module(file, path)
    if not hasattr(_module, "main"):
        raise core.error.SystemLoadWindowError from AttributeError("'main' not in {}".format(_module))
    if not isinstance(_module.main, Window):
        raise core.error.SystemLoadWindowError from TypeError("'main' <{}> is not of type <{}>".format(type(_module.main).__name__, Window.__name__))
    return _module

def module(file: str, path: str=""):
    global _loading_count
    file_path = path + file + ".py"

    try:
        spec = importlib.util.spec_from_file_location("module<{}>".format(_loading_count), PATH+file_path)
        import_path(path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        import_path(path)

        _loading_count += 1
        return module
    except Exception as e:
        raise core.error.SystemLoadModuleError("Module Failed to Load! '{}{}'".format(path, file)) from e

def import_path(path):
    if path in sys.path:
        sys.path.remove(path)
    else:
        sys.path.insert(0, path)
