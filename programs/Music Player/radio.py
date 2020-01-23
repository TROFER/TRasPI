import core
import os
import json

class StartScreen(core.std.Menu):

    def __init__(self):
        with open(f"{core.sys.PATH}programs/Music Player/radio_stations.json", "r") as file:
            self.data = json.load(file)

        elements = []

        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data = value,
                select = PlayerWindow))
        super().__init__(*elements, title="Radio Stations")

    @core.render.Window.focus
    def show(self):
        super().show()
        core.hardware.Backlight.fill(225, 225, 225)

class PlayerWindow(core.render.Window):

    template = core.asset.Template("std::window")
    core.asset.Image("play", path=f"{core.sys.PATH}programs/Music Player/assets/player_play.icon")
    core.asset.Image("stop", path=f"{core.sys.PATH}programs/Music Player/assets/player_stop.icon")
    core.asset.Image(
        "cursor", path=f"{core.sys.PATH}core/resource/image/cursor.icon")

    class ScrollingText(core.element.TextBox):

        def __init__(self, info):
            self.start = 0
            self.info = info
            if len(self.info) < 10:
                self.end = len()
            self.text_time = time.time()
            super().__init__(core.Vector(64, 15), self.info[self.start:self.end])

    def __init__(self, url, info):
        self.url = url
        self.cursor_pos = 0
        self.info = info
        self.volume = 50
        self.header = ScrollingText(self.playlist[self.track_number].description)
        self.title = core.element.Text(core.Vector(3, 5), "Radio Player", justify="L")
        self.buttons = [core.element.Image(core.Vector(42, 50), core.asset.Image("play")),
        core.element.Image(core.Vector(84, 50), core.asset.Image("stop"))]
        self.cursor = core.element.Image(core.Vector(42 * (self.cursor_pos + 1), 18), core.asset.Image("cursor"))

    def volume_up(self):
        if self.volume <= 95:
            self.volume += 5
            os.system(f"amixer set Master {self.volume}%")

    def volume_down(self):
        if self.volume >= 5:
            self.volume -= 5
            os.system(f"amixer set Master {self.volume}%")

    def left(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def right(self):
        if self.cursor_pos < 2:
            self.cursor_pos += 1

    def select(self):
        if self.cursor_pos == 0:
            os.system(f"mpc play {self.url}")
        else:
            os.system(f"mpc stop")
            os.system(f"mpc clear")

    def render(self):
        self.header.render()
        self.title.render()
        for button in self.buttons:
            button.render()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = StartScreen

    def press(self):
        self.window.left()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = StartScreen

    def press(self):
        self.window.right()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = StartScreen

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = StartScreen

    def press(self):
        self.window.volume_up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = StartScreen

    def press(self):
        self.window.volume_down()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = StartScreen

    def press(self):
        self.window.finish()

main = StartScreen()
