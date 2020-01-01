import json
import os
import core

@core.render.Window.focus
def execute(element, window):
    try:
        os.system(element.data)
        yield core.std.Info("Executed")
    except:
        yield core.std.Error("Unknown Error")

class CommandCenter(core.std.Menu):

    def __init__(self):
        with open(f"{core.sys.PATH}programs/command_center/commands.json", "r") as file:
            self.data = json.load(file)

        elements = []

        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data = value,
                select = execute))
        super().__init__(*elements, title="Imported Commands")

    @core.render.Window.focus
    def show(self):
        super().show()
        core.hardware.Backlight.fill(225, 225, 225)

main = CommandCenter()
