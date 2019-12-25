import core
import os
from pygame import mixer
mixer.init()




class PlayerWindow(core.render.Window):

    def __init__(self, element, window):
        self.music = music
        self.state = "STOP"
        #Elements
        self.title = core.element.Text(core.Vector(64, 16), self.music)
        self.buttons =[core.element.TextBox(core.Vector(32, 50), "||", rect_colour=1),
        core.element.TextBox(core.Vector(64, 50), ">",  rect_colour=1),
        core.element.TextBox(core.Vector(96, 50), "STOP", rect_colour=0)]

    def pause(self):
        pass

    def play(self):
        print("Playing")
        pygame.mixer.Sound.play(self.music)

    def stop(self):
        print("Stoping")
        pygame.mixer.Sound.stop(self.music)


    def render(self):
        for button in self.buttons:
            button.render()
        title.render()


@core.render.Window.focus
def play_track(element, window):
    PlayerWindow(element.data)

class MusicList(core.std.Menu):

    def __init__(self):
        mixer.init()

        self.music_index = []

        self.load_music()

        elements = []

        for music in self.music_index:
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), self.music_index, justify="L"),
                data = self.music_index,
                select = play_track)
        super().__init__(*elements, title="Music Player")

    @core.render.Window.focus
    def show(self):
        super().show()
        core.hardware.Backlight.fill(225, 225, 225)
        # This function is run when the window is first loaded

    def load_music(self):
        for music in os.listdir(f"{core.sys.PATH}user/music"):
            print(music)
            if '.mp3' or '.wav' in music:
                try:
                    print("Loading Tracks")
                    self.music_index.append(mixer.Sound(f"{core.sys.PATH}user/music/{music}"))
                    print("Done")
                except ValueError:
                    print("Failed to load some tracks")
        print(self.music_index)

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = PlayerWindow

    def press(self):
        self.window.pause()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = PlayerWindow

    def press(self):
        self.window.play()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = PlayerWindow

    def press(self):
        self.window.stop()

main = MusicList()
