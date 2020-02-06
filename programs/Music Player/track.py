import pygame
import core
import os

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
        self.description = f"{self.name}"
        self.track = None

    def play(self):
        if self.track is None:
            self.track = pygame.mixer.Sound(self.path)
            self.length = self.track.get_length()
        self.track.play()