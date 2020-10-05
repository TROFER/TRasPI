import core
import time
import pygame
from core.render.element import Line, Text
from core.std import popup
from core.hw import Backlight
    
class Main(core.render.Window):

    def __init__(self, playlist):
        super.__init__()
        self.player = Player(playlist)
        self.elements = []
        self.timeout = 0
    
    def render(self):
        pass

    def active(self):
        if self.timeout >= App.const.screen_timeout:
            Backlight.fill([App.const.colour, 1, 0.3])
            self.timeout = -1
        elif self.timeout == -1:
            pass
        else:
            self.timeout += 1

            


class Player:

    def __init__(self, playlist):
        self.playlist = playlist
        self.track_number = 0
        self.state = 0
        self.pausestart = 0
    
    def play(self):
        if self.state == 0:
            try:
                self.playlist[self.track_number].play()
                self.endpoint = self.playlist[self.track_number].length + time.time()
            except FileNotFoundError:
                await popup.Error("File not found")
                return
        elif self.state == 1:
            self.endpoint += time.time() - self.pausestart
            self.pausestart = 0
            pygame.mixer.music.unpause()
            self.state = 2
    
    def pause(self):
        self.pausestart = time.time()
        pygame.mixer.music.pause()
        self.state = 1
    
    def stop(self):
        pygame.mixer.music.stop()
        self.state = 0
        self.track_number = 0
    
    def skip(self):
        if self.track_number != len(self.playlist) - 1:
            self.stop()
            self.track_number += 1
            self.play()
        else:
            await popup.Info("End of queue")