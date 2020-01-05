from core.sys import PATH
import core.system.log import Log
from core.render.window import Window
import importlib.util

loading_count = 0
@core.render.Window.focus
def load(program: str, path: str="programs", file: str="main"):
    global loading_count
    path = "{}{}/{}/main.py".format(PATH, path, program)
    try:
        spec = importlib.util.spec_from_file_location("module<{}:{}>".format(loading_count, program), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "main"):
            return AttributeError("'main' not in {}".format(module))
        if not isinstance(module.main, Window):
            return TypeError("'main' <{}> is not of type <{}>".format(type(module.main).__name__, Window.__name__))
        loading_count += 1
        return module.main
    except FileNotFoundError:
        return FileNotFoundError("'{}.py' not in '{}{}'".format(file, path, program))
    except GeneratorExit:
        pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt Raised: Exiting")
    except BaseException as error:
        Log.Error(program, error)
        yield core.std.Error("Program Error")
    return None
