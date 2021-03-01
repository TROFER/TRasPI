import core
from generation import scene
from elements import backlight, paralax
from controls import keyboard

class Room(core.render.Window):

    def __init__(self, depth):
        super().__init__()

class Transition(core.render.Window):

    def __init__(self, depth):
        self.depth = depth
        self.generate()
    
    def generate(self):
        if self.depth == 0:
            
        if self.depth > 4:
            scene.Transition([random.choice([True, False]) for i in range(4)])
        



