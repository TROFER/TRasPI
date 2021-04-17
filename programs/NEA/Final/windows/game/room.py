import asyncio
import random
import time

import core
from app import App
from core.hw import Key as KeyBacklight
from elements.game import Backlight, Paralax, ParalaxLayer, Player, MainLoop
from generation import scene
from windows.game.transiton import Transition

from game import common, keyboard


class Room(core.render.Window):

    MinSegments = 3
    MaxSegments = 5
    GlobalSpeed = 8
    InputRateLimit = 0.5
    FloorHeight = 55
    HitBoxSize = 16
    ScoreValue = 1

    def __init__(self, game):
        super().__init__()
        self.discovered = False  # Once discovered set to time
        self.game = game
        self.handles = Handles(self)
        self.position = 0
        self.hitbox = {
            "left-exit": None,
            "right-exit": None
        }
        if App.const.debug:
            App.interval(self.debug)

    async def show(self):
        # Set Keybindings
        keyboard.Hotkey("esc", self.finish)
        keyboard.Hotkey("w", self.handles.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("a", self.handles.left, rate_limit=self.InputRateLimit)
        keyboard.Hotkey("d", self.handles.right,
                        rate_limit=self.InputRateLimit)

        #await asyncio.sleep(6)

        # Check for hints
        self.hint()

        # Set Banner and Score
        if self.discovered:
            pass
            #self.elements_conditional["banner"].text = self.discovered
        else:
            # Generate Transition
            #self.transition = Transition(self.game)
            # self.transition.generate()
            # Set Banner Text
            #self.elements_conditional["banner"].text = "New Room Discovered"
            self.discovered = time.strftime("%H:%M")
            # Increment Game Score
            self.game.score += self.ScoreValue
            # Show a banner. New room or already visited.

    def render(self):
        core.Interface.render(self.mainloop)

    def generate(self):
        # Generate Room
        segments = random.randint(self.MinSegments, self.MaxSegments)
        self.scene = scene.Room(segments)
        self.width = 128 * segments

        # Create Exit Hitboxes
        self.hitbox["left-exit"] = (0, self.HitBoxSize)
        self.hitbox["right-exit"] = ((self.width) -
                                     self.HitBoxSize, (self.width))
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

        # Render
        self.elements = [self.paralax, self.backlight, self.player]
        self.mainloop = MainLoop(self.elements)

    def hint(self):
        if self.hitbox["left-exit"][0] <= self.position <= self.hitbox["left-exit"][1]:
            KeyBacklight.all(True)

        elif self.hitbox["right-exit"][0] <= self.position <= self.hitbox["right-exit"][1]:
            KeyBacklight.all(True)

        else:
            KeyBacklight.all(False)

    def debug(self):
        common.restart_line()
        self.game.print_debug()
        print(
            f"[room] Pos: {self.position}, Width: {self.width}, Discovered: {self.discovered}")


class Handles:

    def __init__(self, room):
        self.room = room

    async def interact(self):
        room = self.room

        if room.Hitbox["left-exit"][0] < room.position > room.Hitbox["left-exit"][1]:
            room.finish()
            
        elif room.Hitbox["right-exit"][0] < room.position > room.Hitbox["right-exit"][0]:
            await room.transition

    def right(self):
        room = self.room

        # Room
        if room.position + room.GlobalSpeed < room.width:
            room.position += room.GlobalSpeed

        # Player Sprite
        if room.position < 64 or room.width - room.position < 64:
            room.player.increment()

        # Paralax
        if room.position > 64:
            room.paralax.increment()

        # Backlight
        room.backlight.increment()
        self._any()

    def left(self):
        room = self.room
        
        # Room
        if room.position - room.GlobalSpeed > 0:
            room.position -= room.GlobalSpeed

        # Player Sprite
        if room.position < 64 or room.width - room.position < 64:
            room.player.decrement()

        # Paralax
        if (room.width) - room.position > 64:
            room.paralax.decrement()

        # Backlight
        room.backlight.decrement()
        self._any()

    def _any(self):
        room = self.room
        # Check for hints
        room.hint()
