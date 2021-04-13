import random

from app import App
from core import Vector
from game.library import lib
from generation.common import align
from PIL import Image as PIL


class Player(core.render.Primative):

    def __init__(self, height, speed: float = 5):
        super().__init__()
        self.x = 0
        self.y = height
        self.speed = speed
        if App.var.playerskin is None:
            type_id = lib.fetch_typeid("asset", "player-skin")
            lib.databases["textures"].c.execute(
                "SELECT image_id FROM asset WHERE type_id = ?", [type_id])
            image_id = random.choice(lib.databases["textures"].c.fetchall())[0]
            App.var.playerskin = image_id
        self.sprite = lib.fetch_image(App.var.playerskin)
        self.x_offset = align(self.sprite, "X", "C")
        self.y_offset = align(self.sprite, "Y", "B")

    def render(self, draw):
        frame = PIL.new("RGBA", (128, 64))
        frame.alpha_compositie(self.sprite, dest=(
            self.x + self.x_offset,
            self.y + self.y_offset))
        draw.im.paste(frame.convert("1").im, (0, 0, *frame.size))

    def increment(self):
        if self.x + int(self.speed) < 128 - self.sprite.width:
            self.x += self.speed

    def decrement(self):
        if self.x - int(self.speed) < 0:
            self.x -= self.speed

    def set_position(self, position):
        self.x = position

    def copy(self):
        return self.sprite
