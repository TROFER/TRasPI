import sys
from core.sys import PATH
from core.render.window import Window
import importlib.util

loading_count = 0
def load(program: str, path: str="programs", file: str="main"):
    global loading_count
    path = "{}{}/{}/".format(PATH, path, program)
    file_path = path + "main.py"
    try:
        spec = importlib.util.spec_from_file_location("module<{}:{}>".format(loading_count, program), file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "main"):
            return AttributeError("'main' not in {}".format(module))
        if not isinstance(module.main, Window):
            return TypeError("'main' <{}> is not of type <{}>".format(type(module.main).__name__, Window.__name__))
        loading_count += 1
        sys.path.insert(0, path)
        return module.main
        # sys.path.remove(path) # ADD THIS LATER
    except FileNotFoundError:
        return FileNotFoundError("'{}.py' not in '{}{}'".format(file, path, program))
    return None
