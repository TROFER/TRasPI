import os
import time
import pygame

import single_track
#Needs player window
#Needs track class

class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = path[-4:]
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

class Main(core.render.Window):

    def __init__(self):
        self.window = single_track.SingleTrack()
        self.run()
        self.finish()

    @core.render.Window.focus
    def run(self):
        yeild self.window