import os
import time


class Player(core.render.Window):

    class Volume:

        def __init__(self, step=5):
            self.volume = 75
            self.step = step
            self.set()

        def set(self):
            os.system(f"amixer set Master {self.volume}%")

        def get(self):
            return self.volume

        def decrese(self):
            self.volume -= self.step
            self.set()

        def increse(self):
            self.volume += self.step
            self.step()

    class SText(core.element.Text):

        def __init__(self, pos, text, width):
            self.begin = 0
            self.time = time.time()
            self.text = text
            if len(self.text) < width:
                self.end = len(self.text)
            else:
                self.end = width
            super().__init__(core.Vector(
                pos[0], pos[1]), self.text[self.start:self.end])

        def render(self):
            if time.time() - self.time > 1:  # Speed
                if self.start < len(self.text):
                    self.start += 1
                else:
                    self.start = 0
                if self.end < len(self.text):
                    self.start += 1
                else:
                    self.end = 0
            self.render()

    def __init__(self, station):
        core.asset.Image(
            "play", path=f"{core.sys.PATH}programs/Music Player/assets/player_play.icon")
        core.asset.Image(
            "stop", path=f"{core.sys.PATH}programs/Music Player/assets/player_stop.icon")
        self.volume = Volume()
        self.state = 0
        element_control_centre = [core.asset.Image(
            "stop"), core.asset.Image("play")]
        elements = [
            core.element.Text(core.Vector(64, 3), station[0]),
            core.element.Line(core.Vector(3, 47),
                              core.Vector(125, 47), width=2),
            core.element.Text(core.Vector(102, 57), self.volume.get()),
            core.element.Image(core.Vector(63, 55),
                               element_control_centre[self.state])
        ]

    def render(self):
        for element in elements:
            element.render()


class StartScreen(core.std.Menu):

    def __init__(self):
        self.index()
        elements = []
        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data=(key, value),
                select=self.play))
        super().__init__(*elements, title="Music Player -Radio-")

    @core.render.Window.focus
    def index(self):
        try:
            with open(f"{core.sys.PATH}programs/Music Player/radio_stations.json", "r") as file:
                self.data = json.load(file)
        except IOError:
            window = core.std.Error("No Stations")
            yield window
            self.window.finish()

    @core.render.Window.focus
    def play(self, element, window):
        window = Player(element.data)
        yield window

    @core.render.Window.focus
    def show(self):
        super().show()
