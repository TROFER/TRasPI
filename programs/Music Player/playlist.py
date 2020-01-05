import core
from programs.music_player import main
# Needs to import main from main import Track, PlayerWindow

class StartScreen(core.std.Menu): #Open playlist window
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

    for playlist in self.library:
        elements.append(core.std.Menu.Element(
            core.element.Text(core.Vector(0, 0), playlist.name, justify="L"),
            data = track,
            select = self.start))

    super().__init__(*elements, title="Open Playlist")

    @core.render.Window.focus
    def start(self, element, window):
        player = player.PlayerWindow(element.data) #Needs to pass the playlist (Type List)
        yield player

    @core.render.Window.focus
    def lib_empty(self):
        yield core.std.Warning("Libary is empty")

main = StartScreen()
