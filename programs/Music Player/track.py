import pygame
import core
import os

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
        self.description = f"{self.name}"
        self.track = None

    def length(self):
        self.track = pygame.mixer.Sound(self.path)
        return self.track.get_length()

    def play(self):
        if self.track is None:
            self.track = pygame.mixer.Sound(self.path)
            self.length = self.track.get_length()
        self.track.play()

    def unpause(self):
        pygame.mixer.unpause()

    def pause(self):
        self.track.pause()

    def stop(self):
        self.track.stop()
