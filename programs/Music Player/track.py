import pygame
import core
import os

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
        self.description = f"{self.name}"
        self.track = None

    @core.render.Window.focus
    def play(self):
        if self.track is None:
            try:
                self.track = pygame.mixer.Sound(self.path)
            except IOError:
                window = core.std.Error("Track load error")
                yield window
            self.length = self.track.get_length()
        self.track.play()