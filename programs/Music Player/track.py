import pygame
import core
import os
from tinytag import TinyTag


class Track:

    def __init__(self, filename):
        self.path = f"{core.sys.PATH}user/music/{filename}"
        self.name = os.path.basename(self.path)[:-4]
        try:
            try:
                self.tags = TinyTag.get(self.path)
                self.length = self.tags.duration
                self.description = f"{self.name}, {self.tags.title}, {self.tags.artist}, {self.tags.genre}, {self.tags.year}"
            except UnicodeDecodeError:
                print(self.name)
                self.name = "UTF-8 Error"
                self.length = 1
                self.description = f"Error Reading Metadata"
        except FileNotFoundError:
            self.description = ""
            self.length = 1
        except BaseException as e:
            print(e)

    @core.render.Window.focus
    def play(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
