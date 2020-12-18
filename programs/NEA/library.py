import sqlite3
from PIL import Image as PIL
import os
import sys

CD = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"


class Library:

    DB_PATH = f"{CD}/gamedata/assets.db"
    IMPORT_PATH = f"{CD}/import/"
    ASSET_TYPES = ["foreground", "background", "base", "furniture"]

    def __init__(self):
        self.load(self.DB_PATH)

    def load(self, path):
        try:
            self.db = sqlite3.connect(path)
            self.c = self.db.cursor()
        except sqlite3.OperationalError:
            self.build()
        return self.db, self.c

    def build(self):
        open(self.DB_PATH, 'wb')
        self.c.execute("""CREATE TABLE image(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data BLOB,
            width INTEGER,
            height INTEGER
            )""")
        self.c.execute("""CREATE TABLE type(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT,
            end INTEGER
            )""")
        self.c.execute("""CREATE TABLE theme(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT UNIQUE
            )""")
        self.c.execute("""CREATE TABLE asset(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            type_id INTEGER,
            theme_id INTEGER,
            image_id INTEGER,
            FOREIGN KEY (type_id) REFERENCES  type(id),
            FOREIGN KEY (theme_id) REFERENCES theme(id),
            FOREIGN KEY (image_id) REFERENCES image(id)
            )""")
        for _type in self.ASSET_TYPES:
            self.c.execute(
                "INSERT INTO type (name, end) VALUES (?, ?)", [_type, False])
        for _type in self.ASSET_TYPES:
            self.c.execute(
                "INSERT INTO type (name, end) VALUES (?, ?)", [_type, True])
        assets = self.index(self.IMPORT_PATH)
        self.db.commit()

    def import_asset(self, path, _type, _theme, end=None):
        self.c.execute("SELECT id FROM type WHERE name = ? AND end = ?", [_type, end])
        type_id = self.c.fetchone()[0]
        self.c.execute("SELECT id FROM theme WHERE name = ?", [_theme])
        theme_id = self.c.fetchone()[0]
        image = PIL.open(path).convert("RGBA")
        width, height = image.width, image.height
        self.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
                       image.tobytes(), width, height])
        image_id = self.c.lastrowid()
        self.c.execute("INSERT INTO asset (type_id, theme_id, image_id) VALUES (?, ?, ?)", [
                       type_id, theme_id, image_id])

    def index(self, path):
        for _theme in os.scandir(path):
            if _theme.is_dir():
                for _type in os.scandir(f"{self.IMPORT_PATH}/{_theme.name}"):
                    if _type.is_dir() and _type.name.lower() in self.ASSET_TYPES:
                        for _asset in os.scandir(f"{self.IMPORT_PATH}/{_theme.name}"):
                            self.import_asset(
                                _asset.path, _type.name, _theme.name, end=True if "end" in _asset.name else False)


library = Library()
library.build()
