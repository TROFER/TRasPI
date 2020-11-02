import core
import os
import sqlite3
from app import App
from tinytag import TinyTag, TinyTagException

class Library:

    DATBASE_PATH = f"{core.sys.const.path}programs/Music Player/resource/db/library.db"

    def __init__(self):
        try:
            self.db = sqlite3.connect(self.DATBASE_PATH)
            self.c = self.db.cursor()
            if App.var.rescan or next(self.c.execute("SELECT count(*) FROM track"))[0] == 0:
                self.rescan()
        except (FileNotFoundError, sqlite3.OperationalError):
            self.rebuild()
        App.var.rescan = False
        self.c.close()
        self.db.commit()

    def rebuild(self):
        open(self.DATBASE_PATH, 'wb').close()
        self.db = sqlite3.connect(self.DATBASE_PATH)
        self.c = self.db.cursor()
        self.c.execute("""
            CREATE TABLE genre(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name text UNIQUE
            )
        """)
        self.c.execute("""
            CREATE TABLE album(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name text UNIQUE
            )
        """)
        self.c.execute("""
            CREATE TABLE tags(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                duration int,
                artist text,
                year text,
                bitrate int,
                size float
            )
        """)
        self.c.execute("""
            CREATE TABLE track(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                title text,
                path text,
                description text,
                genre_id int,
                album_id int,
                tags_id int,
                FOREIGN KEY (genre_id) REFERENCES genre(id),
                FOREIGN KEY (album_id) REFERENCES album(id),
                FOREIGN KEY (tags_id) REFERENCES tags(id)
            )
        """)
        self.c.execute("""
            CREATE TABLE playlist(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                tracks INT
            )
        """)    
        self.c.execute("""
            CREATE TABLE radio(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name text,
                url text,
                genre_id int,
                FOREIGN KEY (genre_id) REFERENCES genre(id)
            )
        """)
        self.rescan(clear=False)

    def rescan(self, clear=True):
        if clear:
            self.c.execute("DELETE FROM track"), self.c.execute("DELETE FROM genre"), self.c.execute("DELETE FROM album"), self.c.execute("DELETE FROM tags")
        for _track in self._index([".wav", ".flac"]):
            try:
                self._add_track(Track(_track))
            except ImportError:
                continue
        for _stations in self._index([".station"]):
            with open(_stations, 'r') as file:
                for station in file.read().splitlines():
                    try:
                        self._add_station(station)
                    except ImportError:
                        continue
        self.c.close()
        self.db.commit()

    def _add_track(self, track):
        try:
            self.c.execute("INSERT INTO genre (name) values (?)", [track.genre])
        except sqlite3.IntegrityError:
            pass
        self.c.execute("SELECT id FROM genre WHERE name = ?", [track.genre])
        track.genre = self.c.fetchone()[0]
        try:
            self.c.execute("INSERT INTO album (name) values (?)", [track.album])
        except sqlite3.IntegrityError:
            pass
        self.c.execute("SELECT id FROM album WHERE name = ?", [track.album])
        track.album = self.c.fetchone()[0]
        self.c.execute("""INSERT INTO tags (
            duration,
            artist,
            year,
            bitrate,
            size) VALUES (?, ?, ?, ?, ?)""", [track.tags.duration, track.tags.artist, track.tags.year, track.tags.bitrate, track.tags.filesize])
        self.c.execute("SELECT id FROM tags ORDER BY id DESC LIMIT 1")
        track.tags = self.c.fetchone()[0]
        self.c.execute("""INSERT INTO track (
            title,
            path,
            description,
            genre_id,
            album_id,
            tags_id) VALUES (?, ?, ?, ?, ?, ?)""", [track.title, track.path, track.desc, track.genre, track.album, track.tags])

    def _add_station(self, station):
        _station = Station(*station.split("|"))
        if len(_attr) != 3:
            raise ImportError
        try:
            self.c.execute("INSERT INTO genre (name) values (?)", [_station.genre])
        except sqlite3.IntegrityError:
            pass
        self.c.execute("SELECT id FROM genre WHERE name = ?", [_station.genre])
        _station.genre = self.c.fetchone()[0]
        self.c.execute("""INSERT INTO radio (
            name,
            url,
            genre_id) VALUES (?, ?, ?)""", [_station.name, _station.url, _station.genre])
            
    def _index(self, extension: list):
        _tracks = []
        for _dir in [f"{core.sys.const.path}user/music"]:
            _tracks += self._recr(_dir, extension)
        return _tracks
    
    def _recr(self, path, extension):
        _tracks = []
        for item in os.scandir(path):
            if item.is_file():
                if any(suffix in item.name for suffix in extension):
                    _tracks.append(f"{path}/{item.name}")
            elif item.is_dir():
                _tracks += self._recr(f"{path}/{item.name}", extension)
        return _tracks
    
class Track:

    def __init__(self, path):
        self.title = ".".join(path.split("/")[-1].split(".")[:-1])
        self.path = path
        try:
            self.tags = TinyTag.get(path)
        except TinyTagException:
            print(path)
        self.genre, self.album = self.tags.genre, self.tags.album
        if self.genre is None or self.album is None:
            raise ImportError
        self.desc = self.title if self.tags.title is None else self.tags.title
        for attr in [self.tags.artist, self.tags.year, f"{round(self.tags.filesize / 1048576, 2)}Mb"]:
            if attr is not None:
                self.desc += f", {attr}"
        self.desc += " "

class Station:

    def __init__(self, name, url, catgeory):
        self.name, self.url, self.genre = name, url, catgeory
