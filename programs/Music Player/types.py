import pygame
from tinytag import TinyTag


class Track:

    def __init__(self, path):
        self.path = path
        self.name = path.split("/")[-1][0:-4]
        self.format = path.split("/")[-1][-4:]
        try:
            self.meta_tags = TinyTag.get(self.path)
            self.length = self.meta_tags.duration
            self.desc = f"{self.meta_tags.title}, {self.meta_tags.artist}, {self.meta_tags.album}"
            if self.meta_tags.year is not None:
                self.desc += f", {self.meta_tags.year}"
        except UnicodeDecodeError:
            return UnicodeDecodeError
        except FileNotFoundError:
            return FileNotFoundError

    def play(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()


class Album:

    def __init__(self, name, items):
        self.name = name
        self.items = items


class Genre:

    def __init__(self, name, items):
        self.name = name
        self.items = items


class Playlist:

    def __init__(self, name, tracks):
        self.name = name
        self.tracks = tracks
