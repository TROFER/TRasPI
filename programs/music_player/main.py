import core
import os
import programs.music_player.player
import programs.music_player.track
import time

class PlaylistScreen(core.std.Menu):
    self.library = []
    elements = []
    try:
        for file in os.listdir(f"{core.sys.PATH}user/music/playlists"):
            if ".json" in file:
                playlist = []
                for tracks in json.load(file):
                    trackinstance = track.Track(tracks)
                    playlist.append(trackinstance)
                self.libary.append(playlist)
    except:
        self.lib_empty()
        self.finish()

    for playlist in self.library:
        elements.append(core.std.Menu.Element(
            core.element.Text(core.Vector(0, 0), playlist.name, justify="L"),
            data = track,
            select = self.start))
        super().__init__(*elements, title="Open Playlist")

    @core.render.Window.focus
    def start(self, element, window):
        player = player.PlayerWindow(element.data)
        yield player

    @core.render.Window.focus
    def lib_empty(self):
        yield core.std.Warning("Libary is empty")


class StartScreen(core.render.Window):

    template = core.asset.Template("std::window", path="window.template")
    cursor = core.asset.Image("cursor", path=f"{core.sys.PATH}programs/music_player/assets/cursor.icon")
    quit = core.asset.Image("quit", path=f"{core.sys.PATH}programs/music_player/assets/quit.icon")
    radio = core.asset.Image("radio", path=f"{core.sys.PATH}programs/music_player/assets/radio.icon")
    track = core.asset.Image("track", path=f"{core.sys.PATH}programs/music_player/assets/track.icon")
    playlist = core.asset.Image("playlist", path=f"{core.sys.PATH}programs/music_player/assets/playlist.icon")

    def __init__(self):
        self.index = 1
        self.labels = ['Open Radio', 'Open Music File', 'Open Playlist', 'Quit']
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "Music Player", justify="L")
        self.body = [core.element.Image(core.Vector(25, 32), core.asset.Image("radio")),
        core.element.Image(core.Vector(50, 32), core.asset.Image("track")),
        core.element.Image(core.Vector(75, 32), core.asset.Image("playlist")),
        core.element.Image(core.Vector(100, 32), core.asset.Image("quit"))]
        self.current_item = core.element.TextBox(core.Vector(64, 50), self.labels[self.index])
        self.cursor = core.element.Image(core.Vector(25 * (self.index + 1), 18), core.asset.Image("cursor"))

    def render(self):
        self.title.render()
        for icon in self.body:
            icon.render()
        self.current_item = core.element.TextBox(core.Vector(64, 50), self.labels[self.index])
        self.cursor = core.element.Image(core.Vector(25 * (self.index + 1), 18), core.asset.Image("cursor"))
        self.current_item.render(), self.cursor.render()

    def select(self):
        if self.index == 2:
            window = PlayerWindow()
            yield window

    def up(self):
        if self.index < len(self.labels) - 1:
            self.index += 1

    def down(self):
        if self.index != 0:
            self.index -= 1

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = StartScreen

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = StartScreen

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = StartScreen

    def press(self):
        self.window.down()

main = StartScreen()
