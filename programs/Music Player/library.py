import core
import os
import sqlite3
from app import App
from tinytag import TinyTag

class Library:

    DATBASE_PATH = f"{core.sys.const.path}programs/Music Player/resource/db/library.db"

    def __init__(self):
        try:
            self.db = sqlite3.connect(self.DATBASE_PATH)
            self.c = self.db.cursor()
            try:
                if App.var.rescan or next(self.c.execute("SELECT count(*) FROM track"))[0] == 0:
                    self.rescan()
            except sqlite3.OperationalError:
                self.rebuild()
        except FileNotFoundError:
            self.rebuild()
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
                size int
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
        for _track in self._index():
            self._add_track(Track(_track)) 
        self.c.close()
        self.db.commit()

    def rescan(self):
        self.c.execute("DELETE FROM track"), self.c.execute("DELETE FROM genre"), self.c.execute("DELETE FROM album"), self.c.execute("DELETE FROM tags")
        for _track in self._index():
            self._add_track(Track(_track)) 
        self.c.close()
        self.db.commit()

    def _add_track(self, track):
        try:
            self.c.execute("INSERT INTO genre (name) values (?)", [track.genre])
            track.genre = next(self.c.execute("SELECT id FROM genre WHERE name = ?", [track.genre]))[0]
        except sqlite3.IntegrityError:
            track.genre = next(self.c.execute("SELECT id FROM genre WHERE name = ?", [track.genre]))[0]
        try:
            self.c.execute("INSERT INTO album (name) values (?)", [track.album])
            track.album = next(self.c.execute("SELECT id FROM album WHERE name = ?", [track.album]))[0]
        except sqlite3.IntegrityError:
            track.album = next(self.c.execute("SELECT id FROM album WHERE name = ?", [track.album]))[0]
        self.c.execute("""INSERT INTO tags (
            duration,
            artist,
            year,
            bitrate,
            size) VALUES (?, ?, ?, ?, ?)""", [track.tags.duration, track.tags.artist, track.tags.year, track.tags.bitrate, track.tags.filesize])
        track.tags = next(self.c.execute("SELECT id FROM tags ORDER BY id DESC LIMIT 1"))[0]
        self.c.execute("""INSERT INTO track (
            title,
            path,
            description,
            genre_id,
            album_id,
            tags_id) VALUES (?, ?, ?, ?, ?, ?)""", [track.title, track.path, track.desc, track.genre, track.album, track.tags])
                
    def _index(self):
        _tracks = []
        for _dir in [f"{core.sys.const.path}user/music"]:
            _tracks += self._recr(_dir)
        return _tracks
    
    def _recr(self, path):
        _tracks = []
        for item in os.scandir(path):
            if item.is_file():
                if ".ogg" in item.name or ".mp3" in item.name:
                    _tracks.append(f"{path}/{item.name}")
            elif item.is_dir():
                _tracks += self._recr(f"{path}/{item.name}")
        return _tracks
    
class Track:

    def __init__(self, path):
        self.title = path.split("/")[-1][0:-4]
        self.path = path
        self.tags = TinyTag.get(path)
        self.genre, self.album = self.tags.genre, self.tags.album
        self.desc = self.tags.title
        for attr in [self.tags.artist, self.tags.year, self.tags.filesize]:
            if attr is not None:
                self.desc += f", {attr}"
