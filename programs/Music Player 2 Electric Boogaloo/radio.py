import os
import time


class RadioPlayer(core.render.Window):

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

        def update(self):
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
            "play", path=f"{core.sys.PATH}programs/Music Player/asset/play.icon")
        core.asset.Image(
            "stop", path=f"{core.sys.PATH}programs/Music Player/asset/stop.icon")
        self.volume = Volume()
        self.state = False
        self.url = station[1]
        self.element_control_centre = [core.asset.Image(
            "stop"), core.asset.Image("play")]
        self.stext = SText((65, 39), station[0], 10)
        self.elements = [
            core.element.Text(core.Vector(64, 3), station[0]),
            core.element.Line(core.Vector(3, 47),
                              core.Vector(125, 47), width=2),
            core.element.Text(core.Vector(102, 57), self.volume.get()),
            core.element.Image(core.Vector(63, 55),
                               self.element_control_centre[int(self.state)])
        ]

    def render(self):
        for element in self.elements:
            element.render()
        self.stext.update()

    def vol_up(self):
        self.volume.increse()

    def vol_down(self):
        self.volume.decrese()

    def toggle(self):
        self.state != self.state
        if self.state:
            os.system(f"mpc play {self.url}")
        else:
            os.system(f"mpc stop"), os.system(f"mpc clear")


class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = RadioPlayer
    def press(self):
        self.window.finish()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = RadioPlayer

    def press(self):
        self.window.toggle()


class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = RadioPlayer

    def press(self):
        self.window.vol_up()


class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = RadioPlayer

    def press(self):
        self.window.vol_down()


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
        window = RadioPlayer(element.data)
        yield window

    @core.render.Window.focus
    def show(self):
        super().show()
