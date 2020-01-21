import core
import os

import core.sys.log # TEMP

core.asset.Image("std::script", path="pyfile.icon")
core.asset.Image("std::folder", path="folder.icon")
core.asset.Image("std::return", path="return.icon")

__all__ = ["ProgramMenu"]

class ProgramMenu(core.std.Menu):

    def __init__(self, path="programs/"):
        elements = []

        for diritem in os.listdir(core.sys.PATH + path):
            item_path = path + diritem
            print(item_path)

            if os.path.isdir(core.sys.PATH + item_path):
                if "main.py" in os.listdir(core.sys.PATH + item_path): # Script
                    image, func = "std::script", self._select_program
                else: # Folder
                    image, func = "std::folder", self._select_folder

            elements.append(core.std.Menu.Element(
                core.element.Image(core.Vector(4, 0), core.asset.Image(image)),
                core.element.Text(core.Vector(10, 0), diritem.title(), justify="L"),
                data = item_path,
                select = func
            ))

        elements.append(core.std.Menu.Element(
            core.element.Image(core.Vector(4, 0), core.asset.Image("std::return")),
            core.element.Text(core.Vector(10, 0), "Return", justify="L"),
            select = lambda s,w: w.finish()
        ))

        super().__init__(*elements, title=path, end=False)

    @core.render.Window.focus
    def _select_folder(self, element, window):
        yield ProgramMenu(element.data+"/")
    @core.render.Window.focus
    def _select_program(self, element, window):
        try:
            program = core.asset.Program("Module", path=element.data+"/")
        except core.error.SystemLoadError as e:
            print(core.sys.log.exception_info(e))
            core.sys.log.Log.log(e)
            return (yield core.std.Error("LOAD"))

        program.import_path()
        try:
            yield program.window
        except 
        program.import_path()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = ProgramMenu

    def press(self):
        pass