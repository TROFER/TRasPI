import datetime

import core
from core import Vector
from app import App
from core.render.element import Line, Text

from game import keyboard, library


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.scores = self.load_scores()
        self.index = 0
        self._flag = False

        # Elements 
        self.title = Text(Vector(64, 3), "Scoreboard")
        self.position = Text(Vector(3, 15), "Position: ", justify="L")
        self.name = Text(Vector(3, 25), "Name: ", justify="L")
        self.score = Text(Vector(3, 35), "Score: ", justify="L")
        self.date = Text(Vector(3, 45), "Date: ", justify="L")

        self.elements = [self.title, Line(Vector(0, 7), Vector(128, 7)), self.position, self.name, self.score, self.date]

        App.interval(self.check_flag, 0.1)
    
    async def show(self):
        # Reset
        self._flag = False
        self._refresh()
        keyboard.clear_all()

        # Bind Hotkeys
        keyboard.Hotkey("esc", self.done)
        keyboard.Hotkey("w", self.up)
        keyboard.Hotkey("s", self.down)

        # Set Backlight
        core.hw.Backlight.fill((57, 99, 100), force=True)
    
    def render(self):
        for element in self.elements:
            core.interface.render(element)

    def load_scores(self):
        scores_db = library.lib.databases["scores"]
        scores_db.c.execute("SELECT * FROM score ORDER BY score DESC")
        return scores_db.c.fetchall()
    
    def done(self):
        self._flag = True
    
    def up(self):
        if self.index != 0:
            self.index -= 1
            self._refresh()
    
    def down(self):
        if self.index != len(self.scores) - 1:
            self.index += 1
            self._refresh()

    def _refresh(self):
        try:
            self.position.text = f"Position: {ordinal(self.index + 1)}"
            self.name.text = f"Name: {self.scores[self.index][2]}"
            self.score.text = f"Score: {self.scores[self.index][3]}"
            timestamp = datetime.datetime.fromtimestamp(self.scores[self.index][1])
            self.date.text = f"Date: {timestamp.strftime('%d/%m/%Y')}"
        except IndexError:
            pass

    async def check_flag(self):
        if self._flag:
            self.finish()
    
def ordinal(number):
    _map = {
        "1" : "st",
        "2" : "nd",
        "3" : "rd"
    }
    try:
        _ord = _map[str(number)[-1]]
    except KeyError:
        _ord = "th"
    return f"{number}{_ord}"
