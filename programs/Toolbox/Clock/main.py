import core
import json
import time

default = "default"
timeout = True


class Main(core.render.Window):

    def __init__(self):
        self.timer = 0
        self.timeout = 0
        self.data = self.ldr(default)
        if self.data is not None:
            # core.asset.Font("font", self.data["clock"]["font"])
            core.asset.Template("template", path=self.data["background"])
            core.hardware.Backlight.gradient([int(val) for val in self.data["backlight"][0]], saturation=int(self.data["backlight"][1]), value=int(self.data["backlight"][2]))
            self.elements = [(core.element.Text(core.Vector(int(val) for val in element["pos"]), "LDR", element["font"],
                                          element["size"], element["colour"], element["justify"]), element["format"]) for element in self.data["elements"]]
                                    

    def active(self):
        core.hardware.Backlight.gradient(self.data["backlight"])
        self.timeout = 0

    def inactive(self):
        core.hardware.Backlight.gradient(self.data["backlight"], value=0.5)

    def ldr(self, name):
        try:
            with open(f"{core.sys.PATH}programs/Toolbox/Clock/package/{name}/clock.cfg") as file:
                return json.load(file)
        except FileNotFoundError:
            # yield core.std.Error("Default Missing")
            print("FileNotFound")
        except json.JSONDecodeError:
            print("JSONDecodeError")
            # yield core.std.Error("Bad JSON format")

# core.asset.Font("font"),

    def render(self):
        while not time.time() - self.timer > 1:
            time.sleep(time.time() - self.timer)
        for element in self.elements:
            element[0].text(time.strftime(element[1]))
            element[1].render()
        if self.timeout > 60:
            self.timeout += 1
        else:
            if timeout:
                self.inactive()
        self.timer = time.time()


class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Main

    def press(self):
        self.window.finish()


main = Main()
