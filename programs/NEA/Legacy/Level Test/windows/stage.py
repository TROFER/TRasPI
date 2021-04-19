import asyncio
import random

import core
import util
from elements import backlight, paralax
from generation import scene


class Room(core.render.Window):

    MinWidth = 2
    MaxWidth = 5

    def __init__(self, game):
        self.discovered = False # Once discovered set to time 
        self.game = game

    async def show(self):
        await asyncio.sleep(3)
        # Show a banner. New room or already visited.
    
    def render(self):
        for element in self.elements:
            core.Interface.render(element)
    
    def generate(self):
        # Generate Room
        self.width = random.randint(self.MinWidth, self.MaxWidth)
        self.scene = scene.Room(self.width)
        # Graphical Elements
        self.paralax = paralax.Paralax([
            paralax.ParalaxLayer(self.scene.base, speed=0.75),
            paralax.ParalaxLayer(self.scene.background, speed=2),
            paralax.ParalaxLayer(self.scene.fixings, speed=3),
            paralax.ParalaxLayer(self.scene.foreground, speed=5)
        ])
        self.backlight = backlight.Backlight(util.colour_strip(self.scene.base), y=64)
        self.elements = [self.paralax]



