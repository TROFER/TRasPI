import pygame
import core
import os

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
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
