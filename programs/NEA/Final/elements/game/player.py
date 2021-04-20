import random

import core
from app import App
from core import Vector
from game.library import lib
from generation.common import align
from PIL import Image as PIL


class Player:

    def __init__(self, height, speed: float):
        self.x, self.y = 0, height
        self.speed = speed
        self.rotation = "Forward"

        if App.var.playerskin is None:
            type_id = lib.fetch_typeid("texture", "player-skin")
            lib.databases["textures"].c.execute(
                "SELECT image_id FROM texture WHERE type_id = ?", [type_id])
            image_id = random.choice(lib.databases["textures"].c.fetchall())[0]
            App.var.playerskin = image_id
        self.sprite = lib.fetch_image(App.var.playerskin)
        self.y += align(self.sprite, "Y", "B")
        self.x_offset = align(self.sprite, "X", "C")

    def render(self, frame):
        construct = PIL.new("RGBA", (256, 64))
        construct.alpha_composite(self.sprite, dest=(self.x + 128 + self.x_offset, self.y))
        construct = construct.crop((128, 0, 256, 64))
        frame.alpha_composite(construct)
        return frame

    def set_position(self, position):
        self.x = position
    
    def increment(self):
        self.x += self.speed
    
    def decrement(self):
        self.x -= self.speed
    
    def flip_backward(self):
        if self.rotation != "Backward":
            self.sprite = self.sprite.transpose(PIL.FLIP_LEFT_RIGHT)
            self.rotation = "Backward"
    
    def flip_forward(self):
        if self.rotation != "Forward":
            self.sprite = self.sprite.transpose(PIL.FLIP_LEFT_RIGHT)
            self.rotation = "Forward"