import asyncio
import random
import time

import core
from app import App
from core.hw import Key as KeyBacklight
from elements.game import (Animation, Backlight, MainLoop, Paralax,
                           ParalaxLayer, Player)
from generation import scene

from game import common, keyboard


class Room(core.render.Window):

    MinSegments = 2
    MaxSegments = 4
    GlobalSpeed = 16
    InputRateLimit = 1
    FloorHeight = 55
    HitBoxSize = 16
    ScoreValue = 1

    def __init__(self, game):
        super().__init__()
        self.discovered = False  # Once discovered set to time
        self.game = game
        self.handle = RoomHandle(self)
        self.flag = None
        self.position = 0
        self.hitbox = {
            "left-exit": None,
            "right-exit": None
        }
        # Initiate Flag Checking
        App.interval(self.check_flag, 0.1)

    async def show(self):
        # Reset 
        self.flag = None

        # Set Keybindings
        keyboard.Hotkey("esc", lambda: None)
        keyboard.Hotkey("e", self.handle.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("a", self.handle.left, rate_limit=self.InputRateLimit)
        keyboard.Hotkey("d", self.handle.right,
                        rate_limit=self.InputRateLimit)
        # Check for hints
        self.hint()

        # Set Banner and Score
        if self.discovered:
            pass
            #self.elements_conditional["banner"].text = self.discovered
        else:
            # Generate Transition
            self.transition = Transition(self.game)
            self.transition.generate()
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

    async def check_flag(self):
        if self.flag is not None:
            KeyBacklight.all(False)
            if self.flag.asynchronous:
                await self.flag.function
            else:
                self.flag.function()

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


class RoomHandle:

    def __init__(self, room):
        self.room = room

    def interact(self):
        room = self.room

        if room.hitbox["left-exit"][0] <= room.position <= room.hitbox["left-exit"][1]:
            room.flag = Flag(room.finish)

        elif room.hitbox["right-exit"][0] <= room.position <= room.hitbox["right-exit"][1]:
            room.flag = Flag(room.transition, True)

    def right(self):
        room = self.room

        # Room
        if room.position + room.GlobalSpeed < room.width:
            room.position += room.GlobalSpeed

        # Player Sprite
        if room.position + room.GlobalSpeed <= 64 or room.width - room.position <= 64:
            room.player.increment()

        # Paralax
        if room.position + room.GlobalSpeed > 64:
            room.paralax.increment()

        # Backlight
        if room.position + room.GlobalSpeed <= 64 and room.width - room.position <= 64:
            room.backlight.increment()
        self._any()

    def left(self):
        room = self.room

        # Room
        if room.position - room.GlobalSpeed <= 0:
            room.position -= room.GlobalSpeed

        # Player Sprite
        if room.position <= 64 or room.width - room.position <= 64:
            room.player.decrement()

        # Paralax
        if (room.width - room.position) + room.GlobalSpeed >= 64:
            room.paralax.decrement()

        # Backlight
        if room.position >= 64:
            room.backlight.decrement()
        self._any()

    def _any(self):
        room = self.room
        # Check for hints
        room.hint()
        # Print Debug
        if App.const.debug:
            room.debug()


class Transition(core.render.Window):

    InputRateLimit = 1
    AnimationSpeed = 0.7
    FloorHeight = 55
    PlayerSpeed = 8

    def __init__(self, game):
        super().__init__()
        self.discovered = False
        self.game = game
        self.handle = TransitionHandle(self)
        self.flag = None
        self.position = 0
        self.mapping = {
            "left-exit": [(21, 42), None],
            "center-exit": [(42, 84), None],
            "right-exit": [(84, 107), None]
        }

    async def show(self):
        # Reset 
        self.flag = None

        # Set Keybindings
        keyboard.Hotkey("esc", lambda: None)
        keyboard.Hotkey("e", self.handle.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("a", self.handle.left, rate_limit=self.InputRateLimit)
        keyboard.Hotkey("d", self.handle.right, rate_limit=self.InputRateLimit)

        # Generate Subrooms

        if not self.discovered:
            for value in self.mapping.values():
                if value[1] == self.finish:
                    self.player.set_position((value[0][1] - value[0][0]) // 2) # Approximate Door Position
                elif value[1] is not None:
                    value[1].generate()

            self.discovered = True

        # Initiate Flag Checking
        App.interval(self.check_flag, 0.1)

    def render(self):
        core.Interface.render(self.mainloop)

    def generate(self):
        # Generate Mapping
        self.mapping[random.choice(list(self.mapping.keys()))][1] = self.finish
        for key, value in zip(self.mapping.keys(), self.mapping.values()):
            if value[1] is None:
                if random.choice([True, False]):
                    self.mapping[key][1] = Room(self.game)

        # Generate Transition
        self.scene = scene.Transition(
            [False if value[1] is None else True for value in self.mapping.values()])

        # Graphical Elements

        # Background & Foreground Animation
        self.background = Animation(
            self.scene.background_frames, speed=self.AnimationSpeed)
        self.foreground = Animation(
            self.scene.foreground_frames, speed=self.AnimationSpeed)

        # Player
        self.player = Player(self.FloorHeight, self.PlayerSpeed)

        # Render
        self.elements = [self.background, self.player, self.foreground]
        self.mainloop = MainLoop(self.elements)

    async def check_flag(self):
        if self.flag is not None:
            if self.flag.asynchronous:
                await self.flag.function
            else:
                self.flag.function()


class TransitionHandle:

    def __init__(self, transition):
        self.transition = transition

    def interact(self):
        transition = self.transition
        transition.flag = Flag(transition.finish)

    def right(self):
        transition = self.transition
        transition.player.increment()
        self._any()

    def left(self):
        transition = self.transition
        transition.player.decrement()
        self._any()

    def _any(self):
        transition = self.transition


class Flag:

    def __init__(self, function: callable, asynchronous: bool = False):
        self.function = function
        self.asynchronous = asynchronous
