import asyncio
import random
import time

import common
import core
from core.hw import Key
from core.render.element import Image
from elements import Backlight, Paralax, ParalaxLayer, Player
from generation import scene
from windows.game import Transition

from game import keyboard


class Room(core.render.Window):

    MinWidth = 2
    MaxWidth = 5
    GlobalSpeed = 5
    FloorHeight = 50
    Hitbox = {
        "left-exit": None,
        "right-exit": None
    }
    ScoreValue = 1

    def __init__(self, game):
        super().__init__()
        self.discovered = False  # Once discovered set to time
        self.game = game
        self.handles = Handles(self)
        self.position = 0

    async def show(self):
        # Set Keybindings
        keyboard.Unbind()
        keyboard.Hotkey("esc", self.game.pause_menu)
        keyboard.Hotkey("W", self.handles.interact)
        keyboard.Hotkey("A", self.handles.decrement)
        keyboard.Hotkey("D", self.handles.increment)
        # Check for hints
        self.hint()
        await asyncio.sleep(3)
        if self.discovered:
            self.elements_conditional["banner"].text = self.discovered
        else:
            # Generate Transition
            self.transition = Transition(self.game)
            self.transition.generate()
            # Set Banner Text
            self.elements_conditional["banner"].text = "New Room Discovered"
            self.discovered = time.strftime("%H:%M")
            # Increment Game Score
            self.game.score += self.ScoreValue
        # Show a banner. New room or already visited.

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def generate(self):
        # Generate Room
        self.width = random.randint(self.MinWidth, self.MaxWidth)
        self.scene = scene.Room(self.width)
        # Create Hitboxes
        self.Hitbox["left-exit"] = (0, 10)
        self.Hitbox["right-exit"] = (self.width - 10, self.width)
        # Graphical Elements
        # Paralax
        self.paralax = Paralax([
            ParalaxLayer(self.scene.base, offset=0.3),
            ParalaxLayer(self.scene.background, offset=0.6),
            ParalaxLayer(self.scene.fixings, offset=0.7),
            ParalaxLayer(self.scene.foreground, offset=1)
        ], self.GlobalSpeed)
        # Backlight
        self.backlight = Backlight(
            common.colour_strip(self.scene.base, y=64), self.GlobalSpeed)
        # Player 
        self.player = Player(self.FloorHeight, self.GlobalSpeed)
        self.elements = [self.paralax, self.backlight, self.player]
        self.elements_conditional = {
            "banner": Banner(core.Vector(64, 20))
        }

    def hint(self):
        if self.Hitbox["left-exit"][0] < self.position > self.Hitbox["left-exit"][1]:
            Key.all(True)
        elif self.Hitbox["right-exit"][0] < self.position > self.Hitbox["right-exit"][1]:
            Key.all(True)
        else:
            key.all(False)
        


class Handles:

    def __init__(self, room):
        self.r = room

    async def interact(self):
        if self.r.Hitbox["left-exit"][0] < self.r.position > self.r.Hitbox["left-exit"][1]:
            self.r.finish()
        elif self.r.Hitbox["right-exit"][0] < self.r.position > self.r.Hitbox["right-exit"][0]:
            await self.room.transition

    def right(self):
        # Player Sprite
        if self.r.position < 32 - self.r.GlobalSpeed:
            self.r.player.increment()
        elif self.r.width - self.r.position < 32:
            self.r.player.increment()
        else:
            self.r.player.set_position(32)
        # Paralax
        self.r.paralax.increment()
        # Backlight
        self.r.backlight.increment()
        self._any()

    def left(self):
        # Player Sprite
        if self.r.position < 32:
            self.r.player.decrement()
        elif self.r.width - self.r.position < 32:
            self.r.player.decrement()
        else:
            self.r.player.set_position(32)
        # Paralax
        self.r.paralax.decrement()
        # Backlight
        self.r.backlight.decrement()
        self._any()
    
    def _any(self):
        # Check for hints 
        self.r.hint()
