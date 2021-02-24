import os
import sqlite3

from PIL import Image as PIL


class Library:

    IMPORT_PATH = f"D:/Documents/Programing/Python/TrasPi Operating System/programs/NEA/Level Test/import/"
    DB_PATH = f"D:/Documents/Programing/Python/TrasPi Operating System/programs/NEA/Level Test/resource/assets.db"
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
        self.c.execute("""CREATE TABLE transition(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            north_exit INTEGER,
            south_exit INTEGER,
            left_exit INTEGER,
            right_exit INTEGER,
            FOREIGN KEY (north_exit) REFERENCES asset(id),
            FOREIGN KEY (south_exit) REFERENCES asset(id),
            FOREIGN KEY (left_exit) REFERENCES asset(id),
            FOREIGN KEY (right_exit) REFERENCES asset(id)
            )""")
        self.c.execute("""CREATE TABLE frame(
            transition_id INTEGER,
            asset_id INTEGER,
            FOREIGN KEY (transition_id) REFERENCES transition(id),
            FOREIGN KEY (asset_id) REFERENCES asset(id)
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
        return self.c.lastrowid

    def load_assets(self, path):
        for _item in os.scandir(path):
            if "transitions" in _item.name and _item.is_dir():
                for transition in os.scandir(_item.path):
                    for _file in os.scandir(transition.path):
                        if "top" in _file.name:
                            ne_assetID = self.import_asset(_file.path)
                        elif "down" in _file.name:
                            se_assetID = self.import_asset(_file.path)
                        elif "left" in _file.name:
                            le_assetID = self.import_asset(_file.path)
                        elif "right" in _file.name:
                            re_assetID = self.import_asset(_file.path)
                    self.c.execute("INSERT INTO transition (north_exit, south_exit, left_exit, right_exit) VALUES(?, ?, ?, ?)",
                                   [ne_assetID, se_assetID, le_assetID, re_assetID])
                    transition_id = self.c.lastrowid
                    for frame in os.scandir(transition.path + "/frames"):
                        print(f"Found frame for {transition.name}")
                        asset_id = self.import_asset(
                            frame.path, "transition", transition.name)
                        self.c.execute("INSERT INTO frame (transition_id, asset_id) VALUES (?, ?)", [
                                       transition_id, asset_id])
            elif _item.is_dir():
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
