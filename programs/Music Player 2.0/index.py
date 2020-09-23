import os
#import core
#import pygame
from tinytag import TinyTag

class Index:

    DEFAULT_PATH = f"{core.sys.const.path}user/music"

    @classmethod
    def scan(self, path=None):
        if path is None:
            path = self.DEFAULT_PATH
        library = []
        for genre in os.scandir(path):
            if genre.is_dir():
                albums = []
                for album in os.scandir(f"{path}/{genre.name}"):
                    if album.is_dir():
                        tracks = []
                        for track in os.scandir(f"{path}/{genre.name}/{album.name}"):
                            if ".ogg" in track.name or ".mp3" in track.name:
                                res = Track(f"{path}/{genre.name}/{album.name}/{track.name}")
                                if not isinstance(res, UnicodeDecodeError) and not isinstance(res, FileNotFoundError):
                                    tracks.append(res)
                        albums.append([album.name, tracks])                    
                library.append([genre.name, albums])
        return library

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