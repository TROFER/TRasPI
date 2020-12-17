import sqlite3

DB_PATH = "gamedata/"

def load():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    return db, cursor

def build():
    open(DB_PATH, 'wb')
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()
    c.execute("""CREATE TABLE image(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        data BLOB,
        width INTEGER,
        height INTEGER
        )""")
    c.execute("""CREATE TABLE type(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name UNIQUE,
        corner INTEGER
        )""")

def inde