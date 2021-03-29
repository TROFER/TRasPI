import os
import sqlite3

from PIL import Image as PIL


class Library:

    IMPORT_PATH = f"{core.sys.const.path}programs/NEA/import/"
    DB_PATH = f"{core.sys.const.path}programs/NEA/resouce/db/assets.db"
    ASSET_TYPES = ["foreground", "base", "background",
                   "furniture", "fixing", "palette",
                   "transition", "player"]

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
            center_exit INTEGER,
            left_exit INTEGER,
            right_exit INTEGER,
            FOREIGN KEY (center_exit) REFERENCES image(id),
            FOREIGN KEY (left_exit) REFERENCES image(id),
            FOREIGN KEY (right_exit) REFERENCES image(id)
            )""")
        self.c.execute("""CREATE TABLE frame(
            transition_id INTEGER,
            image_id INTEGER,
            type TEXT,
            FOREIGN KEY (transition_id) REFERENCES transition(id),
            FOREIGN KEY (image_id) REFERENCES image(id)
            )""")
        self.c.execute("""CREATE TABLE player_skins(
            skin id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT,
            image_id,
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
        image_id = self.import_image(path)
        self.c.execute("INSERT INTO asset (type_id, theme_id, image_id) VALUES (?, ?, ?)", [
            type_id, theme_id, image_id])
        return self.c.lastrowid

    def import_image(self, path):
        """Returns Bytesdata, Width, Height"""
        image = PIL.open(path).convert("RGBA")
        self.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
                       image.tobytes(), image.width, image.height])
        return self.c.lastrowid

    def import_player_skin(self, file):
        name = file.name.split(".")[0]
        image_id = self.import_image(file.path)
        self.c.execute("INSERT INTO player_skins (name, image_id) VALUES (?, ?)", [
                       name, image_id])

    def load_assets(self, path):
        _count = 0
        for _item in os.scandir(path):
            if "player" in _item.name and _item.is_dir():
                self.import_player_skin(_item)
            if "transition" in _item.name and _item.is_dir():
                for transition in os.scandir(_item.path):
                    for _file in os.scandir(transition.path):
                        if "center" in _file.name:
                            center_exit = self.import_image(_file.path)
                        elif "left" in _file.name:
                            left_exit = self.import_image(_file.path)
                        elif "right" in _file.name:
                            right_exit = self.import_image(_file.path)
                    self.c.execute("INSERT INTO transition (center_exit, left_exit, right_exit) VALUES(?, ?, ?)",
                                   [center_exit, left_exit, right_exit])
                    transition_id = self.c.lastrowid
                    for frame in os.scandir(transition.path + "/frames/background"):
                        image_id = self.import_image(frame.path)
                        self.c.execute("INSERT INTO frame (transition_id, image_id, type) VALUES (?, ?, ?)", [
                            transition_id, image_id, "bg"])
                    for frame in os.scandir(transition.path + "/frames/foreground"):
                        image_id = self.import_image(frame.path)
                        self.c.execute("INSERT INTO frame (transition_id, image_id, type) VALUES (?, ?, ?)", [
                            transition_id, image_id, "fg"])
            elif _item.is_dir():
                for _type in os.scandir(f"{self.IMPORT_PATH}{_item.name}"):
                    if _type.is_dir() and _type.name.lower() in self.ASSET_TYPES:
                        for _asset in os.scandir(f"{self.IMPORT_PATH}{_item.name}/{_type.name}"):
                            self.import_asset(
                                _asset.path, _type.name, _item.name, end=True if "end" in _asset.name else False)
                            _count += 1
                    if "palette" in _type.name.lower():
                        self.import_asset(_type.path, "palette", _item.name)
        print(f"Assets DB rebuilt. Imported {_count} assets")

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

    def fetch_image(self, image_id):
        self.c.execute(
            "SELECT data, width, height FROM image WHERE id = ?", [image_id])
        _image = self.c.fetchone()
        return PIL.frombytes("RGBA", (_image[1], _image[2]), _image[0])


library = Library()
library.build()
