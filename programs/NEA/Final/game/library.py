import json
import os
import sqlite3
import time

from PIL import Image as PIL


class Library:

    Path = {
        "packages": f"{core.sys.const.path}programs/NEA/assets/",
        "databases": f"{core.sys.const.path}programs/NEA/resouce/db/"
    }

    def init(self, databases):
        self.databases = databases
        for db in self.databases.items():
            db.db, db.c, rebuild = self.load(db.path)
            if rebuild and db.loader is not None:
                db.loader(db)

    def load(self, path):
        try:
            db = sqlite3.connect(path):
            c = db.cursor()
            return db, c, False
        except sqlite3.OperationalError:
            return self.build(path.split("/")[-1].split(".")[0], path)

    def build(self, name, dest):
        try:
            with open(self.Path["databases"] + name, 'r') as file:
                script = file.read().replace("\n", "").split("%")
            with open(dest, 'w') as file:
                file.write("")
            db, c = self.load(dest)
            for cmd in script:
                c.execute(cmd)
            db.commit()
            return db, c, True
        except FileNotFoundError:
            print("[ERROR] Unable to locate build file")

    def import_texture(self, db, pack_id, texture):
        image = PIL.open(texture.path).convert("RGBA")
        db.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
            image.tobytes(), image.width, image.height
        ])
        image_id = db.c.lastrowid
        texture_type = texture.name.split(".")[-1].lower()
        db.c.execute("SELECT id FROM texture-type WHERE name = ?",
                     [texture_type])
        try:
            type_id = db.c.fetchone()[0]
        except TypeError:
            db.c.execute(
                "INSERT INTO texture-type (name) VALUES (?)", [texture_type])
            type_id = db.c.lastrowid
        if pack_id is not None
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
        count, start = 0, time.time()
        for item in os.scandir(self.Path["packages"]):
            if item.is_dir():
                try:
                    with open(item.path + "/pack.meta") as file:
                        meta = json.load(file)
                    db.c.execute(
                        "SELECT id FROM pack-type WHERE name = ?", [meta["type"]])
                    try:
                        type_id = db.c.fetchone()[0]
                    except TypeError:
                        db.c.execute("INSERT INTO pack-type (name) VALUES (?)",
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
                    print(
                        f"[ERROR] Failed reading package '{item.name}' metadata")
                    continue
                except FileNotFoundError:
                    continue
                for item in os.scandir(item.path):
                    if item.is_file:
                        self.import_texture(db, pack_id, item)
                        count += 1
            if item.is_file():
                self.import_texture(db, None, item)
        print(f"[INFO] Imported {count} textures in {time.time() - start}s")
        db.commit()

    def fetch_image(self, image_id: int):
        """Returns a PIL image object"""
        self.databases["textures"].c.execute("""
        SELECT data, with, height FROM image WHERE id = ?""", [image_id])
        image = self.databases["textures"].c.fetchone()
        return PIL.frombytes("RGBA", (image[1], image[2]), image[0])

    def fetch_typeid(self, table: str, name: str):
        if "texture" in table:
            self.databases["textures"].c.execute("SELECT id FROM texture-types WHERE name = ?",
                                                 [name])
        elif "pack" in table:
            self.databases["textures"].c.execute("SELECT id FROM pack-type WHERE name = ?",
                                                 [name])
        else:
            return None
        return self.databases.c.fetchone()[0]


class Database:

    def __init__(self, path, loader=None):
        self.path = path
        self.loader = loader
        self.db = None
        self.c = None


lib = Library()

databases = {
    "textures": Database(
        f"{core.sys.const.path}programs/NEA/resouce/db/textures.db", lib.load_textures)
}

lib.init(databases)
