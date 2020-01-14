import core
import os

core.asset.Image("std::script", path="pyfile.icon")
core.asset.Image("std::folder", path="folder.icon")
core.asset.Image("std::return", path="return.icon")

VISABLE = 4

class Item:

    def __init__(self, name: str, path: str, icon: core.asset.Image):
        self.name, self.path, self.icon = name, path, icon

class Program(Item):

    def __init__(self, name: str, path: str):
        super().__init__(name, path, core.asset.Image("std::script"))

class Folder(Item):

    def __init__(self, name: str, path: str):
        super().__init__(name, path, core.asset.Image("std::folder"))

class ProgramMenu(core.std.Menu):

    def __init__(self, path="programs"):
        elements = []
        