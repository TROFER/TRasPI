import asyncio
import random
import time

import common
import core
from core.render.element import Image
from elements import Backlight, Paralax, ParalaxLayer
from generation import scene
from game.keyboard import Keyboard, Hotkey


class Room(core.render.Window):

    MinWidth = 2
    MaxWidth = 5

    def __init__(self, game):
        self.discovered = False  # Once discovered set to time
        self.game = game
        self.handles = Handles(self)

    async def show(self):
        # Set Keybindings
        Hotkey("esc", self.game.pause_menu)
        Hotkey("W", self.handles.interact)
        Hotkey("A", self.handles.decrement)
        Hotkey("D", self.handles.increment)
        await asyncio.sleep(3)
        if self.discovered:
            self.elements_conditional["banner"].text = self.discovered
        else:
            self.elements_conditional["banner"].text = "New Room Discovered"
            self.discovered = time.strftime("%H:%M")
        # Show a banner. New room or already visited.

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def generate(self):
        # Generate Room
        self.width = random.randint(self.MinWidth, self.MaxWidth)
        self.scene = scene.Room(self.width)
        # Graphical Elements
        self.paralax = Paralax([
            ParalaxLayer(self.scene.base, speed=0.75),
            ParalaxLayer(self.scene.background, speed=2),
            ParalaxLayer(self.scene.fixings, speed=3),
            ParalaxLayer(self.scene.foreground, speed=5)
        ])
        self.backlight = Backlight(
            common.colour_strip(self.scene.base), y=64)
        self.player = Image(core.Vector(
            0, 0), self.game.player.sprite, just_h='B')
        self.elements = [self.paralax, self.backlight, self.player]
        self.elements_conditional {
            "banner": Banner(core.Vector(64, 20))
        }


class Handles:

    def __init__(self, window):
        self.window = window

    def interact(self):
        pass

    def decrement(self):
        pass

    def increment(self):
        if 