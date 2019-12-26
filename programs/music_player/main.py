import core
import os
import pygame
# import audio_metadata

class PlayerWindow(core.render.Window):

    template = core.asset.Template("std::window")
    pause = core.asset.Image("pause", path=f"{core.sys.PATH}programs/music_player/pause.icon")
    play = core.asset.Image("play", path=f"{core.sys.PATH}programs/music_player/play.icon")
    stop = core.asset.Image("stop", path=f"{core.sys.PATH}programs/music_player/stop.icon")

    def __init__(self, track):
        self.track = track
        self.state = 'ST'
        self.select_index = 1
        self.track.load()
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "Music Player", justify="L")
        self.header = core.element.Text(core.Vector(64, 20), self.track.name)
        self.buttons = [core.element.Image(core.Vector(32, 50), core.asset.Image("pause")),
        core.element.Image(core.Vector(64, 50), core.asset.Image("play")),
        core.element.Image(core.Vector(96, 50), core.asset.Image("stop"))]
        self.cursor = core.element.Text(core.Vector(64, 40), "\\/")

    def left(self):
        if self.select_index > 0:
            self.select_index -= 1
            self.cursor.pos = core.Vector(self.buttons[self.select_index].pos[0], 40)

    def right(self):
        if self.select_index + 1 <= len(self.buttons)-1:
            self.select_index += 1
            self.cursor.pos = core.Vector(self.buttons[self.select_index].pos[0], 40)

    def select(self):
        if self.select_index == 0:
            pygame.mixer.pause()
            self.state = "PA"
        elif self.select_index == 1:
            if self.state == "ST":
                self.track.play()
                self.state = "PL"
            else:
                pygame.mixer.unpause()
                self.state = "PL"
        elif self.select_index == 2:
            pygame.mixer.stop()
            self.state = "ST"

    def render(self):
        for button in self.buttons:
            button.render()
        self.title.render(), self.header.render(), self.cursor.render()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = PlayerWindow

    def press(self):
        self.window.left()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = PlayerWindow

    def press(self):
        self.window.right()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = PlayerWindow

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = PlayerWindow

    def press(self):
        self.window.finish()

class Track:

    def __init__(self, filename, name, artist=None):
        self.filename = filename #Full filename eg. .wav, .mp3
        self.name = name
        self.artist = artist

    @core.render.Window.focus
    def load(self):
        try:
            self.track = pygame.mixer.Sound(f"{core.sys.PATH}user/music/{self.filename}")
        except pygame.error:
            yield core.std.Error("Track Load Error")

    def play(self):
        self.track.play()

    def unpause(self):
        pygame.mixer.unpause()

    def pause(self):
        self.track.pause()

    def stop(self):
        self.track.stop()

class StartScreen(core.std.Menu):

    def __init__(self):
        pygame.mixer.init()
        self.library = []
        elements = []
        for file in os.listdir(f"{core.sys.PATH}user/music/"):
            if ".wav" in file or ".ogg" in file:
                self.library.append(Track(file, file[:len(file)-4]))

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

main = StartScreen()
