import core
import json
import os
import radio
from track import Track
from track import Track
from player import LocalPlayer

class Playlist:

    def __init__(self, tracks, name):
        self.tracks = tracks
        self.name = name

class Main(core.std.Menu):

    def __init__(self):
        self.library = []
        try:
            for file in os.listdir(f"{core.sys.PATH}user/music/playlists"):
                if ".json" in file:
                    _playlist = []
                    with open(f"{core.sys.PATH}user/music/playlists/{file}") as playlist:
                        for tracks in json.load(playlist):
                            track = Track(tracks)
                            _playlist.append(track)
                        self.library.append(Playlist(_playlist, file[:-5]))
        except NotADirectoryError:
            self.lib_error()

        elements = []
        for playlist in self.library:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(
                    0, 0), playlist.name, justify="L"),
                data=track,
                select=self.start))

        super().__init__(*elements, title="Music P.. -Playlist-")

    @core.render.Window.focus
    def subwindow(self):
        window = radio.Main()
        yield window

    @core.render.Window.focus
    def start(self, element, window):
        player = LocalPlayer(element.data)
        yield player

    @core.render.Window.focus
    def lib_error(self):
        yield core.std.Warning("Dir Error")

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Main

    def press(self):
        self.window.finish()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Main

    def press(self):
        self.window.subwindow()
