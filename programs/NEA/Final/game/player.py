import random

from app import App
from core import Vector
from generation.common import align

from game.library import lib


class Player:

    def __init__(self):
        if App.var.playerskin is None:
            type_id = lib.fetch_typeid("asset", "player-skin")
            lib.databases["textures"].c.execute(
                "SELECT image_id FROM asset WHERE type_id = ?", [type_id])
            image_id = random.choice(lib.databases["textures"].c.fetchall())[0]
            App.var.playerskin = image_id
        self.sprite = lib.fetch_image(App.var.playerskin)
        '''self.offset = Vector(align(self.sprite, "X", "C"),
                             align(self.sprite, "Y", "B"))'''

player = Player
