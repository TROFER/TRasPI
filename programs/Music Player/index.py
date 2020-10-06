import os
import core
from types import Genre, Album, Track, Playlist


class Index:

    DEFAULT_PATH = f"{core.sys.const.path}user/music"

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
                                res = Track(
                                    f"{path}/{_genre.name}/{_album.name}/{_track.name}")
                                if not isinstance(res, UnicodeDecodeError) and not isinstance(res, FileNotFoundError):
                                    _tracks.append(res)
                        _albums.append(Album(_album.name, _tracks))
                library.append(Genre(_genre.name, _albums))
        return library
