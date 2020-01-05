import core
import os
import time
from programs.music_player import playlist, radio, single_track

class PlayerWindow(core.render.Window):

    template = core.asset.Template("std::window")
    pause = core.asset.Image("pause", path=f"{core.sys.PATH}programs/music_player/assets/pause.icon")
    play = core.asset.Image("play", path=f"{core.sys.PATH}programs/music_player/assets/play.icon")
    stop = core.asset.Image("stop", path=f"{core.sys.PATH}programs/music_player/assets/stop.icon")
    next = core.asset.Image("next", path=f"{core.sys.PATH}programs/music_player/assets/next.icon")
    cursor = core.asset.Image("cursor", path=f"{core.sys.PATH}programs/music_player/assets/cursor.icon")

    class ScrollingText(core.element.TextBox):

        def __init__(self, info):
            self.start = 0
            self.info = info
            if len(self.info) < 10:
                self.end = len()
            self.text_time = time.time()
            super().__init__(core.Vector(64, 15), self.info[self.start:self.end])

        def update(self, info):
            if time.time() - self.text_time > 1:
                if self.end < self.playlist[self.position].info():
                    self.end += 1
                else:
                    self.end = 0
                if self.start < self.playlist[self.position].info():
                    self.start += 1
                else:
                    self.start = 0
                self.text_time = time.time()

    def __init__(self, playlist):
        self.playlist = playlist
        self.track_number = 0
        self.state = 'ST'
        self.volume = 50
        os.system(f"amixer set Master {self.volume}%")
        self.cursor_pos = 1
        # Scrolling Text
        # Window Elements
        self.header = ScrollingText(self.playlist[self.track_number].description)
        self.track_indicator = core.element.Text(core.Vector(64, 25), f"{self.track_number}/{len(playlist)}")
        self.title = core.element.Text(core.Vector(3, 5), "Music Player", justify="L")
        self.buttons = [core.element.Image(core.Vector(25, 50), core.asset.Image("pause")),
        core.element.Image(core.Vector(50, 50), core.asset.Image("play")),
        core.element.Image(core.Vector(75, 50), core.asset.Image("stop")),
        cor.element.Image(core.Vector(100, 50), core.asset.Image("next"))]
        self.cursor = core.element.Image(core.Vector(25 * (self.cursor_pos + 1), 50), core.asset.Image("cursor"))

    def volume_up(self):
        if self.volume <= 95:
            self.volume += 5
            os.system(f"amixer set Master {self.volume}%")

    def volume_down(self):
        if self.volume >= 5:
            self.volume -= 5
            os.system(f"amixer set Master {self.volume}%")

    def left(self):
        if self.cursor_pos != 0:
            self.cursor_pos -= 1

    def right(self):
        if self.cursor_pos > len(self.buttons) - 1:
            self.cursor_pos += 1

    def select(self):
        if self.cursor_pos == 0:
            pygame.mixer.pause()
            self.state, self.pause_time = 'PA', time.time()
        elif self.cursor_pos == 1:
            if self.state == 'PA': #Run when returning from paused state
                self.endpoint += time.time() - self.pause_time
                self.playlist[self.track_number].unpause()
                self.state = 'PL'
            elif self.state == 'ST': #Run when returning from stoped state
                self.playlist[self.track_number].play()
                self.state = 'PL'
                self.endpoint = time.time() + self.playlist[self.track_number].length()
        elif self.cursor_pos == 2:
            pygame.mixer.stop()
            self.state = 'ST'
        elif self.cursor_pos == 3:
            if self.track_number > len(self.playlist) - 1:
                pygame.mixer.stop()
                self.track_number += 1
                self.playlist[self.track_number].play()
                self.state = 'PL'

    def render():
        if self.state == 'PL':
            if self.endpoint > time.time():
                pygame.mixer.stop()
                self.track_number += 1
                self.playlist[self.track_number].play()
        self.title.render()
        self.header.render()
        for button in self.buttons:
            button.render()
        self.cursor.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = PlayerWindow

    def press(self):
        self.window.select()

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

    key = core.render.Button.UP
    window = PlayerWindow

    def press(self):
        self.window.volume_up()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = PlayerWindow

    def press(self):
        self.window.volume_down()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = PlayerWindow

    def press(self):
        self.window.finish()

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = path[:len(path)-4]
        self.description = f"{' '*3}{self.name}{' '*3}"

    def length(self):
        return self.track.get_length()

    def info(self):
        return self.description

    def play(self):
        self.track = pygame.mixer.Sound(self.path)
        self.track.play()

    def unpause(self):
        pygame.mixer.unpause()

    def pause(self):
        self.track.pause()

    def stop(self):
        self.track.stop()

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
        if self.index == 0:
            window = radio.main
        elif self.index == 1:
            window = single_track.main
        elif self.index == 2:
            window = playlist.main
        elif self.index == 3:
            self.finish()
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
