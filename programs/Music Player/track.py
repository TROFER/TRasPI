import pygame
import core
import os
from tinytag import TinyTag


class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
        try:
            self.tags = TinyTag.get(self.path)
            self.length = self.tags.duration
            self.description = f"{self.tags.title}, {self.tags.artist}, {self.tags.genre}, {self.tags.year}"
        except FileNotFoundError:
            self.description = ""
            self.length = 0

    @core.render.Window.focus
    def play(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
