import core
import json
import radio

class SubwindowPlaylist(core.std.Menu):

    def __init__(self):
        self.library = []
        try:
            for file in os.listdir(f"{core.sys.PATH}user/music/playlists"):
                if ".json" in file:
                    playlist = []
                    for tracks in json.load(file):
                        track = track.Track(tracks)
                        playlist.append(track)
                    self.libary.append(playlist)
        except:
            self.lib_empty(), self.finish()

        elements = []
        for playlist in self.library:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(
                    0, 0), playlist.name, justify="L"),
                data=track,
                select=self.start))

        super().__init__(*elements, title="Open Playlist", right=subwindow)

    @core.render.Window.focus
    def subwindow(self):
        window = radio.main
        yield window

    @core.render.Window.focus
    def start(self, element, window):
        player = player.PlayerWindow(element.data)
        yield player

    @core.render.Window.focus
    def lib_empty(self):
        yield core.std.Warning("Libary is empty")


main = SubwindowPlaylist()
