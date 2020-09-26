import os
import sys
import importlib.util
import pickle
import core.error
from ..error.attributes import SysConstant
from .program import Program
from ..type.application import Application, CreateWindow as ApplicationWindowWrapper
from ..asset import base as _AssetBase
from ..error import logging as log
from .. import std

CACHE_DIR = "resource/program/"

class Load:

    def __init__(self):
        self.__programs = {}
        self.tree = {}
        class __DefaultApp(Application):
            name = "ApplicationDefault"
            window = ApplicationWindowWrapper(std.Error("Invalid Program"))
        __DefaultApp._program._file = "/default"
        self.__default = __DefaultApp._program

    def rescan(self, path: str):
        self.tree[path[:-1]], size = scan_programs(SysConstant.path+path, len(SysConstant.path))
        log.core.info("Found %d Programs in '%s'", size, path)
        return self.tree

    def app(self, *path: str, full=False, default=False) -> Program:
        if full:
            path = path[0]
        else:
            tree = self.tree
            for dir in path:
                tree = tree[dir]
            path = tree
        try:
            if path not in self.__programs:
                return self.load(path)
            return self.__programs[path][0]
        except core.error.load.Load:
            if default:
                return self.__default
            raise

    def load(self, path: str) -> Program:
        program, module = load_app(SysConstant.path + path)
        program._file = path
        if (cache := read_cache(path)):
            program.application.var.__setstate__(cache)
        self.__programs[path] = (program, module)
        return program

    def reload(self, program: Program) -> Program:
        if program._file in self.__programs:
            lprog = self.__programs[program._file][0]
            if lprog is program:
                return program
            program._acquire(lprog)
            return program
        if self.__default == program:
            return program
        program._acquire(self.load(program._file))
        self.__programs[program._file] = (program, *self.__programs[program._file][1:])
        return program

    def close(self, program: Program):
        try:
            del self.__programs[program._file]
            log.core.info("Closing Program: %s", program)
        except KeyError:    pass
        write_cache(program._file, program.application.var.__getstate__())

def scan_programs(path: str, top: int):
    total_size = 0
    apps = {}
    with os.scandir(path) as it:
        for file in it:
            if file.is_dir():
                flag = True
                with os.scandir(path+file.name+"/") as fit:
                    for f in fit:
                        if f.name == "main.py":
                            apps[file.name] = path[top:]+file.name+"/"
                            flag = False
                            total_size += 1
                            break
                if flag:
                    apps[file.name], size = scan_programs(path+file.name+"/", top)
                    total_size += size
    for k,v in tuple(apps.items()):
        if not v:
            del apps[k]
    return apps, total_size

def read_cache(name: str) -> dict:
    path = SysConstant.path + name + CACHE_DIR
    try:
        with open(path+"vcm", "r") as file_manager:
            files = file_manager.readlines()
        data = {}
        for key in files:
            key = key.strip()
            with open(path+key+".vcm", "rb") as file:
                data[key] = pickle.load(file)
        return data
    except (FileNotFoundError, EOFError) as e:
        return None

def write_cache(name: str, data):
    path = SysConstant.path + name + CACHE_DIR
    try:
        with open(path+"vcm", "w") as file_manager:
            for key, value in data.items():
                with open(path+key+".vcm", "wb") as file:
                    pickle.dump(value[0], file)
                file_manager.write(key + "\n")
    except FileNotFoundError:
        os.makedirs(path)
        write_cache(name, data)

def validate_app(module) -> tuple:
    if not hasattr(module, "main"):
        log.core.error("Application Missing 'main' Attribute: %s - %s", module.__name__, module.__file__)
        raise core.error.load.Validate(module.__name__, module.__file__, "An Application must Contain a 'main' Attribute")
    if not issubclass(module.main, Application):
        log.core.error("Application 'main' Attribute not : %s - %s", module.__name__, module.__file__)
        raise core.error.load.Validate(module.__name__, module.__file__, f"'main' Attribute must be of type '{Application.__name__}' not '{module.main.__name__}'")
    return (module.main._program, module)

def load_app(path: str):
    log.core.info("Loading Program: '%s'", path)
    try:
        return validate_app(_load_py_file(path))
    except core.error.load.ModuleFileImport as e:
        log.core.error("%s: %s", type(e).__name__, e)
        log.traceback.error("Failed to Import Module: %s", path, exc_info=e)
        raise

_program_count = 1
def _load_py_file(path: str):
    global _program_count
    try:
        import_path(path, True)
        name = "<{}-{}>".format(path.split("/")[-2], _program_count)
        spec = importlib.util.spec_from_file_location(name, path+"main.py", submodule_search_locations=[])
        module = importlib.util.module_from_spec(spec)
        sys_modules = set(sys.modules)
        sys.modules[name] = module
        previous_name = log._active_program
        log._active_program = name
        spec.loader.exec_module(module)
        log._active_program = previous_name

        _program_count += 1
        return module
    except Exception as e:
        raise core.error.load.ModuleFileImport(name, path) from e
    finally:
        import_path(path, False)
        mpath = path[:-1]
        for n in set(sys.modules) - sys_modules:
            mod = sys.modules[n]
            if hasattr(mod, "__file__") and isinstance(mod.__file__, str) and mpath in mod.__file__:
                try:
                    del sys.modules[n]
                except KeyError:    pass

def import_path(path: str, add: bool):
    _AssetBase.search(path+"resource/{name}/", add)
    if add:
        if path not in sys.path:
            sys.path.append(path)
    else:
        try:
            sys.path.remove(path)
        except ValueError: return


load = Load()
