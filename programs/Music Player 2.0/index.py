import os
import core
import pygame
from tinytag import TinyTag

class Index:

    DEFAULT_PATH = f"{core.sys.const.path}user/music"

    def scan(self):
        library = []
        for genre in os.scandir(self.DEFAULT_PATH):
            if genre.is_dir():
                albums = []
                for album in os.scandir(f"{self.DEFAULT_PATH}/{genre.name}"):
                    if album.is_dir():
                        tracks = []
                        for track in os.scandir(f"{self.DEFAULT_PATH}/{genre.name}/{album.name}"):
                            if ".ogg" in track.name or ".mp3" in track.name or ".wav" in track.name:
                                res = Track(f"{self.DEFAULT_PATH}/{genre.name}/{album.name}/{track.name}"))
                                if not isinstance(res, UnicodeDecodeError) and not isinstance(res, FileNotFoundError):
                                    tracks.append(res)
                        albums.append([album.name, tracks])                    
                library.append([genre.name, albums])

class Track:

    def __init__(self, path):
        self.path = path 
        self.name = path.split("/")[-1][0:-4]
        try:
            self.meta_tags = TinyTag.get(self.path)
            self.length = self.meta_tags.duration
            self.desc = f"{self.meta_tags.name}, {self.meta_tags.title}, {self.meta_tags.artist}, {self.meta_tags.genre}, {self.meta_tags.year}}"
        except UnicodeDecodeError:
            return UnicodeDecodeError
        except FileNotFoundError:
            return FileNotFoundError
        
    def play(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
            
