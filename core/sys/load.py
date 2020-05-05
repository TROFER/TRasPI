import os
import sys
import importlib.util
import pickle
from core.sys.attributes import SysConstant
from core.sys.program import Program
from core.type.application import Application
import core.asset.base

CACHE_DIR = "resource/program/"

class Load:

    def __init__(self):
        self.__programs = {}
        self.tree = {}
        self.rescan("home/")
        self.rescan("programs/")

    def rescan(self, path: str):
        self.tree[path[:-1]] = scan_programs(SysConstant.path+path, len(SysConstant.path))
        return self.tree

    def app(self, *path: str) -> Program:
        tree = self.tree
        for dir in path:
            tree = tree[dir]
        path = tree
        if path not in self.__programs:
            return self.load(path)
        return self.__programs[path][0]

    def load(self, path: str) -> Program:
        app = load_app(SysConstant.path + path)
        app[0]._file = path
        if (cache := read_cache(path)):
            app[0].application.var.__setstate__(cache)
            x = app[0].application.var
        self.__programs[path] = app
        return app[0]

    def reload(self, path: str) -> Program:
        app = load_app(SysConstant.path + path)
        app[0]._file = path
        self.__programs[path] = app
        return app[0]

    def close(self, program: Program):
        app = self.__programs[program._file]
        del self.__programs[program._file]
        x = app[0].application.var
        write_cache(program._file, app[0].application.var.__getstate__())

def scan_programs(path: str, top: int):
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
                            break
                if flag:
                    apps[file.name] = scan_programs(path+file.name+"/", top)
    for k,v in tuple(apps.items()):
        if not v:
            del apps[k]
    return apps

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
        raise AttributeError("An Application must Contain a 'main' Attribute")
    if not issubclass(module.main, Application):
        raise TypeError(f"Main must be of type '{Application.__name__}' not '{module.main.__name__}'")
    return (module.main._program, module)

def load_app(path: str):
    return validate_app(_load_py_file(path))

_program_count = 1
def _load_py_file(path: str):
    global _program_count
    try:
        spec = importlib.util.spec_from_file_location("Program<{}-{}>".format(path.split("/")[-2], _program_count), path + "main.py")
        import_path(path, True)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        import_path(path, False)

        _program_count += 1
        return module
    except Exception as e:
        raise e

def import_path(path: str, add: bool):
    if add:
        if path not in sys.path:
            sys.path.append(path)
            core.asset.base._active_dir.append(path+"resource/")
    else:
        try:
            sys.path.remove(path)
            core.asset.base._active_dir.remove(path+"resource/")
        except ValueError: return

load = Load()
