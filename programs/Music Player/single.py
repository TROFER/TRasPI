import core
import colorsys
import os
import playlist
from track import Track
from player import LocalPlayer

class Main(core.std.Menu):

    def __init__(self):
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        self.library = []
        try:
            for file in os.listdir(f"{core.sys.PATH}user/music/"):
                if ".wav" in file or ".ogg" in file:
                    self.library.append(Track(file))
        except NotADirectoryError:
            self.lib_error()

        elements = []
        for musicfile in self.library:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(
                    0, 0), musicfile.name, justify="L"),
                data=musicfile,
                select=self.start))
        super().__init__(*elements, title="Music Player -Track-", end=False)

    @core.render.Window.focus
    def subwindow(self):
        window = playlist.Main()
        yield window

    @core.render.Window.focus
    def lib_error(self):
        yield core.std.Warning("Dir Error")

    @core.render.Window.focus
    def start(self, element, window):
        player = LocalPlayer([element.data])
        yield player

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Main

    def press(self):
        self.window.finish()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Main

    def press(self):
        self.window.subwindow()
