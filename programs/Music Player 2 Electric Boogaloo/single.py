import core

class Main(core.std.Menu):

    def __init__(self):
        self.libary = []
        try:
            for file in os.listdir(f"{core.sys.PATH}user/music/"):
                if ".wav" in file or ".ogg" in file:
                    self.library.append(Track(file))
        except:
            self.lib_empty()
            self.finish()

        elements = []
        for musicfile in self.libary:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(
                    0, 0), musicfile.name, justify="L"),
                data=musicfile,
                select=start))
        super().__init__(*elements, title="Music Player", left=self.finish, right=self.subwindow)

    @core.render.Window.focus
    def subwindow(self):
        window = playlist.Main()
        yield window

    @core.render.Window.focus
    def lib_empty(self):
        yield core.std.Warning("Libary is empty")

    @core.render.Window.focus
    def start(self, element, window):
        player = LocalPlayer(element.data)
        yield player
