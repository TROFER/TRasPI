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

    def import_asset(self, db, pack_id, asset):
        image = PIL.open(asset.path).convert("RGBA")
        db.c.execute("INSERT INTO image (data, width, height) VALUES (?, ?, ?)", [
            image.tobytes(), image.width, image.height
        ])
        image_id = db.c.lastrowid
        asset_type = asset.name.split(".")[-1].lower()
        db.c.execute("SELECT id FROM asset-type WHERE name = ?", [asset_type])
        try:
            type_id = db.c.fetchone()[0]
        except TypeError:
            db.c.execute(
                "INSERT INTO asset-type (name) VALUES (?)", [asset_type])
            type_id = db.c.lastrowid
        db.c.execute("INSERT INTO asset(pack_id, image_id, type_id) VALUES (?, ?, ?)", [
            pack_id,
            image_id,
            type_id
        ])

    def load_assets(self, db):
        count, start = 0, time.time()
        for package in os.scandir(f"{core.sys.const.path}programs/NEA/assets/"):
            try:
                with open(package.path + "/package.meta") as file:
                    meta = json.load(file)
                db.c.execute(
                    "SELECT id FROM pack-type WHERE name = ?", [meta["type"]])
                try:
                    type_id = db.c.fetchone()[0]
                except TypeError:
                    db.c.execute(
                        "INSERT INTO pack-type (name) VALUES (?)", [meta["type"]])
                    type_id = db.c.lastrowid
                db.c.execute("INSERT INTO pack (name, type_id, author, size) VALUES (?, ?, ?, ?)", [
                    package.name,
                    type_id,
                    meta["author"],
                    os.path.getsize(package.path)
                ])
                pack_id = db.c.lastrowid
            except json.JSONDecodeError:
                print(
                    f"[ERROR] Failed reading package {package.name} metadata")
                continue
            except FileNotFoundError:
                continue
            for item in os.scandir(package.path):
                if item.is_file:
                    self.import_asset(db, pack_id, item)
                    count += 1
            print(f"[INFO] Imported {count} assets in {time.time() - start}s")

    def fetch_image(self, image_id: int):
        """Returns a PIL image object"""
        self.databases["assets"].c.execute("""
        SELECT data, with, height FROM image WHERE id = ?""", [image_id])
        image = self.databases["assets"].c.fetchone()
        return PIL.frombytes("RGBA", (image[1], image[2]), image[0])


class Database:

    def __init__(self, path, loader=None):
        self.path = path
        self.loader = loader
        self.db = None
        self.c = None


lib = Library()

databases = {
    "assets": Database(
        f"{core.sys.const.path}programs/NEA/resouce/db/assets.db", lib.load_assets)
}

lib.init(databases)
