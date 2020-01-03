import core
import time
import os

class PlayerWindow(core.render.Window):

    template = core.asset.Template("std::window")
    pause = core.asset.Image("pause", path=f"{core.sys.PATH}programs/music_player/assets/pause.icon")
    play = core.asset.Image("play", path=f"{core.sys.PATH}programs/music_player/assets/play.icon")
    stop = core.asset.Image("stop", path=f"{core.sys.PATH}programs/music_player/assets/stop.icon")
    next = core.asset.Image("next", path=f"{core.sys.PATH}programs/music_player/assets/next.icon")
    cursor = core.asset.Image("cursor", path=f"{core.sys.PATH}programs/music_player/assets/cursor.icon")

    def next_track(self):
        self.track_index += 1
        self.playlist[self.track_index].play()

    def __init__(self, playlist): # Will load the file into pygame.mixer
        self.playlist = playlist #Consists of track objects 
        self.track_index = 0
        self.curret_state = 'ST'
        self.volume = 50
        os.system(f"amixer set Master {self.volume}%")
        # GUI
        self.cursor_pos = 1
        # Scrolling Text
        self.start = 0
        if len(self.info) < 10:
            self.end = len()
        self.time = time.time()
        self.header = core.element.TextBox(core.Vector(64, 15), self.info[self.start:self.end])
        self.title = core.element.Text(core.Vector(3, 5), "Music Player", justify="L")
        self.buttons = [core.element.Image(core.Vector(25, 50), core.asset.Image("pause")),
        core.element.Image(core.Vector(50, 50), core.asset.Image("play")),
        core.element.Image(core.Vector(75, 50), core.asset.Image("stop")),
        cor.element.Image(core.Vector(100, 50), core.asset.Image("next"))]
        self.cursor = core.element.Image(core.Vector(25 * (self.cursor_index + 1), 50), core.asset.Image("cursor"))

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
        elif self.cursor_pos == 1:
            if self.curret_state != 'PL':
                self.playlist[self.position].play()
                self.curret_state = 'PL'
        elif self.cursor_pos == 2:
            pygame.mixer.stop()
        elif self.cursor_pos == 3:
            if self.track_index > len(self.playlist) - 1:
                self.next_track()


    def render():
        if time.time() - self.time > 1:
            if self.end < self.playlist[self.position].info():
                self.end += 1
            else:
                self.end = 0
            if self.start < self.playlist[self.position].info():
                self.start += 1
            else:
                self.start = 0
            self.time = time.time()
        if time.time() > self.playlist[self.track_index].length():
            self.play_next_track()
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
