import core
import os
import pygame
# import audio_metadata

#@core.render.Window.focus
class PlayerWindow(core.render.Window):

    template = core.asset.Template("std::window")

    def __init__(self, element, window):
        self.track = element.data
        self.state = 'ST'
        self.select_index = 1
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "Music Player", justify="L")
        self.header = core.element.Text(core.Vector(64, 15), self.track.name)
        self.media_controls = [core.element.TextBox(core.Vector(32, 50), "||", rect_colour=1),
        core.element.TextBox(core.Vector(64, 50), ">", rect_colour=0),
        core.element.TextBox(core.Vector(96, 50), "\u25A0", rect_colour=1)]

    def left(self):
        if self.select_index > 0:
            self.media_controls[self.select_index].rect_colour = 1
            self.select_index - 1
            self.media_controls[self.select_index].rect_colour = 0

    def right(self):
        if self.select_index + 1 <= len(self.media_controls)-1:
            self.media_controls[self.select_index].rect_colour = 1
            self.select_index + 1
            self.media_controls[self.select_index].rect_colour = 0

    def select(self):
        if self.select_index == 0:
            self.track.pause()
        elif self.select_index == 1:
            self.track.play()
        elif self.select_index == 2: # Change to else once tested
            self.track.stop()

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

@core.render.Window.focus
class Track:

    def __init__(self, filename, name, artist=None):
        self.filename = filename #Full filename eg. .wav, .mp3
        self.name = name
        self.artist = artist
        try:
            self.track = pygame.mixer.Sound(f"{core.sys.PATH}user/music/{filename}")
        except pygame.error:
            yield core.std.Error("Track Load Error")

    def play(self):
        if PlayerWindow.state == 'PA':
            pygame.mixer.unpause()
            PlayerWindow.state = "PL"
        elif PlayerWindow.state == 'ST':
            self.track.play(self.track)
            PlayerWindow.state = "PL"

    def pause(self):
        self.track.pause()
        PlayerWindow.state = "PA"

    def stop(self):
        self.track.stop()
        PlayerWindow.state = "ST"

class StartScreen(core.std.Menu):

    def __init__(self):
        pygame.mixer.init()
        self.library = []
        for file in os.listdir(f"{core.sys.PATH}user/music/"):
            if ".wav" in file or ".mp3" in file:
                self.library.append(Track(file, file[:len(file)-3]))

        for track in self.library:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), self.track.name, justify="L"),
                data = track,
                select = PlayerWindow))
        super().__init__(*elements, title="Open Track")

main = StartScreen()
