import os
import sqlite3

import core
from PIL import Image as PIL


class Library:

    DB_PATH = f"{core.sys.const.path}programs/NEA/Room Test/resource/assets.db"
    IMPORT_PATH = f"{core.sys.const.path}programs/NEA/Room Test/import/"
    ASSET_TYPES = ["foreground", "base", "background",
                   "furniture", "fixing", "palette", "transition"]

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
        for _type in self.ASSET_TYPES[:-5]:
            self.c.execute(
                "INSERT INTO type (name, end) VALUES (?, ?)", [_type, True])
        self.load_assets(self.IMPORT_PATH)
        self.db.commit()

    def import_asset(self, path, _type, _theme, end=False):
        self.c.execute("SELECT id FROM type WHERE name = ? AND end = ?", [
                       _type, int(end)])
        type_id = self.c.fetchone()[0]
        self.c.execute("SELECT id FROM theme WHERE name = ?", [_theme])
        try:
            theme_id = self.c.fetchone()[0]
        except TypeError:
            self.c.execute("INSERT INTO theme (name) VALUES (?)", [_theme])
            theme_id = self.c.lastrowid
        image = PIL.open(path).convert("RGBA")
        width, height = image.width, image.height
        self.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
            image.tobytes(), width, height])
        image_id = self.c.lastrowid
        self.c.execute("INSERT INTO asset (type_id, theme_id, image_id) VALUES (?, ?, ?)", [
            type_id, theme_id, image_id])

    def load_assets(self, path):
        for _item in os.scandir(path):
            if _item.is_dir():
                for _type in os.scandir(f"{self.IMPORT_PATH}{_item.name}"):
                    if _type.is_dir() and _type.name.lower() in self.ASSET_TYPES:
                        for _asset in os.scandir(f"{self.IMPORT_PATH}{_item.name}/{_type.name}"):
                            print(
                                f"{_type.name.capitalize()} asset found! for theme '{_item.name}' name '{_asset.name}' end = {True if 'end' in _asset.name else False}")
                            self.import_asset(
                                _asset.path, _type.name, _item.name, end=True if "end" in _asset.name else False)
                    if "palette" in _type.name.lower():
                        print(f"Pallete Found! for theme '{_item.name}'")
                        self.import_asset(_type.path, "palette", _item.name)
            elif _item.is_file():
                if "transition" in _item.name:
                    self.import_asset(_item.path, "transition", _item.name)

    def get_typeid(self, name: str, end: int = 0):
        self.c.execute(
            "SELECT id from type WHERE name = ? AND end = ?", [name, end])
        try:
            return self.c.fetchone()[0]
        except TypeError:
            return None

    def count_records(self, table):
        self.c.execute(
            "SELECT count(*) FROM {}".format(table))
        return self.c.fetchone()[0]


library = Library()
library.build()
