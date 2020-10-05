import os
#import core
#import pygame
from tinytag import TinyTag

class Index:

    #DEFAULT_PATH = f"{core.sys.const.path}user/music"
    DEFAULT_PATH = "D:/Music/Library III"

    @classmethod
    def scan(self, path=None):
        if path is None:
            path = self.DEFAULT_PATH
        library = []
        for _genre in os.scandir(path):
            if _genre.is_dir():
                _albums = []
                for _album in os.scandir(f"{path}/{_genre.name}"):
                    if _album.is_dir():
                        _tracks = []
                        for _track in os.scandir(f"{path}/{_genre.name}/{_album.name}"):
                            if ".ogg" in _track.name or ".mp3" in _track.name:
                                res = Track(f"{path}/{_genre.name}/{_album.name}/{_track.name}")
                                if not isinstance(res, UnicodeDecodeError) and not isinstance(res, FileNotFoundError):
                                    _tracks.append(res)
                        _albums.append(Album(_album.name, _tracks))                    
                library.append(Genre(_genre.name, _albums))
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

class Album:

    def __init__(self, name, tracks):
        self.name = name
        self.tracks = tracks

class Genre:

    def __init__(self, name, albums):
        self.name = name
        self.albums = albums

res = Index.scan()
for genre in res:
    for album in genre.albums:
        for track in album.tracks:
            print(track.name)