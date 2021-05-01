# /game/library.py

import json
import os
import sqlite3
import time

import core
from app import App
from PIL import Image as PIL


class Library:

    Path = {
        "packages": f"{core.sys.const.path}programs/NEA/Final/assets/",
        "databases": f"{core.sys.const.path}programs/NEA/Final/resource/db/"
    }

    def init(self, databases: list):
        self.databases = databases
        for db in self.databases.values():
            db.db, db.c, rebuild = self.load(db.path)
            if rebuild and db.loader is not None:
                db.loader(db)

    def load(self, path):
        if os.path.isfile(path):
            db = sqlite3.connect(path)
            c = db.cursor()
            return db, c, False
        else:
            if App.const.debug:
                print("[DEBUG] Rebuilding database")
            return self.build(path.split("/")[-1].split(".")[0], path)

    def build(self, name, dest):
        try:
            with open(self.Path["databases"] + name + ".build", 'r') as file:
                script = file.read().replace("\n", "").split("%")
        except FileNotFoundError as e:
            if App.const.debug:
                print("[DEBUG] - [ERROR] Unable to locate build file")
        with open(dest, 'w') as file:
            file.write("")
        db, c, rebuild = self.load(dest)
        for cmd in script:
            c.execute(cmd)
        db.commit()
        return db, c, True

    def import_texture(self, db, pack_id, texture):
        image = PIL.open(texture.path).convert("RGBA")
        db.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
            image.tobytes(), image.width, image.height
        ])
        image_id = db.c.lastrowid
        texture_type = texture.name.split(".")[-1].lower()
        db.c.execute("SELECT id FROM texturetype WHERE name = ?",
                     [texture_type])
        try:
            type_id = db.c.fetchone()[0]
        except TypeError:
            db.c.execute(
                "INSERT INTO texturetype (name) VALUES (?)", [texture_type])
            type_id = db.c.lastrowid
        if pack_id is not None:
            db.c.execute("INSERT INTO texture(pack_id, image_id, type_id) VALUES (?, ?, ?)", [
                pack_id,
                image_id,
                type_id
            ])
        else:
            db.c.execute("INSERT INTO texture(image_id, type_id) VALUES (?, ?)", [
                image_id,
                type_id
            ])

    def load_textures(self, db):
        blacklist = ["meta"]
        count, start = 0, time.time()
        for item in os.scandir(self.Path["packages"]):
            if item.is_dir():
                try:
                    with open(item.path + "/pack.meta") as file:
                        meta = json.load(file)
                    db.c.execute(
                        "SELECT id FROM packtype WHERE name = ?", [meta["type"]])
                    try:
                        type_id = db.c.fetchone()[0]
                    except TypeError:
                        db.c.execute("INSERT INTO packtype (name) VALUES (?)",
                                     [meta["type"]])
                        type_id = db.c.lastrowid
                    db.c.execute("INSERT INTO pack (name, type_id, author, size) VALUES (?, ?, ?, ?)", [
                        item.name,
                        type_id,
                        meta["author"],
                        os.path.getsize(item.path)
                    ])
                    pack_id = db.c.lastrowid
                except json.JSONDecodeError:
                    if App.const.debug:
                        print(
                            f"[DEBUG] - [ERROR] Failed reading package '{item.name}' metadata")
                    continue
                except FileNotFoundError:
                    continue
                for item in os.scandir(item.path):
                    if item.is_file and not any([extension in item.name for extension in blacklist]):
                        self.import_texture(db, pack_id, item)
                        count += 1
            if item.is_file():
                self.import_texture(db, None, item)
        if App.const.debug:
            print(
                f"[DEBUG] Imported {count} textures in {time.time() - start}s")
        db.db.commit()

    def fetch_image(self, image_id: int):
        """Returns a PIL image object"""
        self.databases["textures"].c.execute("SELECT data, width, height FROM image WHERE id = ?",
                                             [image_id])
        image = self.databases["textures"].c.fetchone()
        return PIL.frombytes("RGBA", (image[1], image[2]), image[0])

    def fetch_typeid(self, table: str, name: str):
        table = table.lower()
        if App.const.debug:
            print(
                f"[DEBUG] - Fetching type_id for table '{table}' with name '{name}'")
        if "texture" in table:
            self.databases["textures"].c.execute("SELECT id FROM texturetype WHERE name = ?",
                                                 [name])
        elif "pack" in table:
            self.databases["textures"].c.execute("SELECT id FROM packtype WHERE name = ?",
                                                 [name])
        else:
            if App.const.debug:
                print(f"[DEBUG] - [Error] '{table}' Invalid table name")
        return self.databases["textures"].c.fetchone()[0]

    def fetch_texture(self, type_id):
        """Fetches a texture without a pack_id"""
        self.databases["textures"].c.execute(
            "SELECT image_id FROM texture WHERE type_id = ?", [type_id])
        image_id = self.databases["textures"].c.fetchone()[0]
        return self.fetch_image(image_id)


class Database:

    def __init__(self, path: str, loader: callable = None):
        self.path = path
        self.loader = loader
        self.db = None
        self.c = None


lib = Library()

databases = {
    "textures": Database(
        f"{core.sys.const.path}programs/NEA/Final/resource/db/textures.db", lib.load_textures),
    "scores": Database(
        f"{core.sys.const.path}programs/NEA/Final/resource/db/scores.db", None)
}

if App.const.rebuild_library:
    os.remove(f"{core.sys.const.path}programs/NEA/Final/resource/db/textures.db")

lib.init(databases)