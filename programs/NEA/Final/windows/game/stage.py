import asyncio
import random
import time

import core
from app import App
from elements.game import Animation, MainLoop, Paralax, ParalaxLayer, Player
from generation import scene
from PIL import Image as PIL

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
        ], common.colour_strip(self.scene.base, y=64), self.GlobalSpeed)

        # Player
        self.player = Player(self.FloorHeight, self.GlobalSpeed)

        # Render
        self.elements = [self.paralax, self.player]
        self.mainloop = MainLoop(self.elements)

    async def check_flag(self):
        if self.flag is not None:
            core.hw.Key.all(False)
            if self.flag.asynchronous:
                res = await self.flag.function
                if res == "quit":
                    self.finish("quit")
            else:
                self.flag.function()

    def hint(self):
        if self.hitbox["left-exit"][0] <= self.position <= self.hitbox["left-exit"][1]:
            core.hw.Key.all(True)

        elif self.hitbox["right-exit"][0] <= self.position <= self.hitbox["right-exit"][1]:
            core.hw.Key.all(True)

        else:
            core.hw.Key.all(False)

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
        if room.position < room.width - room.player.sprite.width:
            room.position += room.GlobalSpeed

        # Paralax
        if 64 <= room.position <= room.width - 64:
            room.paralax.increment()

        # Player
        room.player.flip_forward()

        self._any()

    def left(self):
        room = self.room

        # Room
        if room.position != 0:
            room.position -= room.GlobalSpeed

        # Paralax
        if 64 <= room.position <= room.width - 64:
            room.paralax.decrement()

        # Player
        room.player.flip_backward()

        self._any()

    def _any(self):
        room = self.room

        # Player Sprite
        if room.position <= 64:
            room.player.set_position(
                clamp(0, room.position, 64 + (room.player.sprite.width // 2)))
        elif room.width - room.position <= 64:
            room.player.set_position(
                clamp(0, 128 - (room.width - room.position), 128 - room.player.sprite.width))

        # Check for hints
        room.hint()

        # Print Debug
        if App.const.debug:
            room.debug()


class Transition(core.render.Window):

    InputRateLimit = 0.2
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
            "left-exit": [(21, 42), None, 32],
            "center-exit": [(42, 84), None, 64],
            "right-exit": [(84, 107), None, 96]
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
            for data in self.mapping.values():
                if data[1] == self.finish:
                    # Approximate Door Position
                    self.position = data[2]
                    self.player.set_position(data[2])
                elif data[1] is not None:
                    data[1].generate()

            self.discovered = True

        # Initiate Flag Checking
        App.interval(self.check_flag, 0.1)

    def render(self):
        core.Interface.render(self.mainloop)

    def generate(self):
        # Generate Mapping
        self.mapping[random.choice(list(self.mapping.keys()))][1] = self.finish
        for key, data in zip(self.mapping.keys(), self.mapping.values()):
            if data[1] is None:
                # 3/5 Chance to get an addional door
                if random.choice([True, True, True, True, False]):
                    self.mapping[key][1] = Room(self.game)

        # Generate Transition
        self.scene = scene.Transition(
            [False if data[1] is None else True for data in self.mapping.values()])

        # Graphical Elements

        # Background, Foreground & Backlight Animation
        self.background = Animation("image",
                                    self.scene.background_frames, speed=self.AnimationSpeed)
        self.foreground = Animation("image",
                                    self.scene.foreground_frames, speed=self.AnimationSpeed)
        self.backlight = Animation("backlight",
                                   self.scene.backlight_colours, speed=0.5)

        # Player
        self.player = Player(self.FloorHeight, self.PlayerSpeed)

        # Render
        self.elements = [self.backlight, self.background,
                         self.player, self.foreground]
        self.mainloop = MainLoop(self.elements)

    async def check_flag(self):
        if self.flag is not None:
            if self.flag.asynchronous:
                res = await self.flag.function
                if res == "quit":
                    self.finish("quit")
            else:
                self.flag.function()


class TransitionHandle:

    def __init__(self, transition):
        self.transition = transition

    def interact(self):
        transition = self.transition

        for data in transition.mapping.values():
            if data[0][0] <= transition.position <= data[0][1]:
                if data[1] == transition.finish:
                    transition.flag = Flag(transition.finish)
                else:
                    transition.flag = Flag(data[1], True)

    def right(self):
        # Player

        transition = self.transition
        if transition.position != 128:
            transition.position += transition.PlayerSpeed
            transition.player.increment()

        transition.player.flip_forward()

    def left(self):
        # Player

        transition = self.transition
        if transition.position != 0:
            transition.position -= transition.PlayerSpeed
            transition.player.decrement()

        transition.player.flip_backward()


class Flag:

    def __init__(self, function: callable, asynchronous: bool = False):
        self.function = function
        self.asynchronous = asynchronous


def clamp(_min, data, _max):
    return max(_min, min(data, _max))
