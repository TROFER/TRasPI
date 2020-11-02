import core
from core.std import menu

class Main(menu.Menu):

    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()
        _elements = []
        self.c.execute(f"SELECT * FROM radio")
        for _station in self.c.fetchall():
            self.c.execute()