import core
import os
import time
import subprocess
import json
from volume import Volume
from animatedtext import AnimatedText


class RadioPlayer(core.render.Window):

    def __init__(self, station):
        os.system("mpc clear")
        core.asset.Image(
            "play", path=f"{core.sys.PATH}programs/Music Player/asset/play.icon")
        core.asset.Image(
            "stop", path=f"{core.sys.PATH}programs/Music Player/asset/stop.icon")
        self.volume = Volume()
        self.state = True
        self.url = station[1]
        self.centre = [core.asset.Image("stop"),
                       core.asset.Image("play")]
        self.radio_text = AnimatedText((64, 35), station[0], 20)
        self.time = time.time()
        self.elements = [core.element.Text(core.Vector(64, 3), station[0]),
                         core.element.Line(core.Vector(
                             5, 40), core.Vector(125, 40), width=2),
                         core.element.Text(core.Vector(15, 53), self.volume.get())]
        self.toggle()

    def render(self):
        self.elements[2].text(self.volume.get())
        core.element.Image(core.Vector(64, 53),
                           self.centre[int(self.state)]).render()
        if time.time() - self.time > 1:
            os.system("mpc status")
            self.radio_text.edit(subprocess.check_output(
                "mpc status", shell=True).decode().splitlines()[0])
            self.time = time.time()
        for element in self.elements:
            element.render()
        self.radio_text.update()

    def vol_up(self):
        self.volume.increse()

    def vol_down(self):
        self.volume.decrese()

    def toggle(self):
        if self.state:
            os.system(f"mpc add {self.url}"), os.system(f"mpc play")
            self.radio_text.toggle(True)
        else:
            os.system(f"mpc stop"), os.system(f"mpc clear")
            self.radio_text.toggle(False)
        self.state = not self.state


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


class Main(core.std.Menu):

    def __init__(self):
        self.index()
        elements = []
        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data=(key, value),
                select=self.play))
        super().__init__(*elements, title="Music Player -Radio-", end=False)

    @core.render.Window.focus
    def index(self):
        try:
            with open(f"{core.sys.PATH}programs/Music Player/data/stations.json", "r") as file:
                self.data = json.load(file)
        except IOError:
            window = core.std.Error("No Stations")
            self.data = {}
            yield window

    @core.render.Window.focus
    def play(self, element, window):
        window = RadioPlayer(element.data)
        yield window


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Main

    def press(self):
        self.window.finish()
