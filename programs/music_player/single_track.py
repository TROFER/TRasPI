import core
from programs.music_player import main
# Needs to import main from main import Track, PlayerWindow

class StartScreen(core.std.Menu):

    def __init__(self):
        self.library = []
        elements = []
        try:
            for file in os.listdir(f"{core.sys.PATH}user/music/"):
                if ".wav" in file or ".ogg" in file:
                    self.library.append(Track(file, file[:len(file)-4]))
        except:
            self.lib_empty()
            self.finish()

        for track in self.library:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), track.name, justify="L"),
                data = track,
                select = self.start))
        super().__init__(*elements, title="Open Track")

    @core.render.Window.focus
    def start(self, element, window):
        player = PlayerWindow(element.data)
        yield player

    @core.render.Window.focus
    def lib_empty(self):
        yield core.std.Warning("Libary is empty")

main = StartScreen()
