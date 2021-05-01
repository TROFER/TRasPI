# /windows/game/stage.py

import asyncio
import random
import time

import core
from app import App
from elements.game import Animation, MainLoop, Parallax, ParallaxLayer, Sprite
from generation import scene
from PIL import Image as PIL

from game import common, keyboard, handles, items


class Stage(core.render.Window):

    InputRateLimit = 1

    def __init__(self, game, handle):
        super().__init__()
        self.discovered = False
        self.game = game
        self.handle = handle(self)
        self.flag = None
        self.position = 0

    def _show(self):
        # Reset
        self.flag = None

        # Set Keybindings
        keyboard.Hotkey("esc", self.handle.esc)
        keyboard.Hotkey("e", self.handle.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("e", self.handle.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("a", self.handle.left,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("d", self.handle.right,
                        rate_limit=self.InputRateLimit)

        # Update Game Active Window
        self.game.active_window = self

        # Start Flag Checking
        App.interval(self.check_flag, 0.1)

    async def check_flag(self):
        if self.flag is not None:
            if self.flag.asynchronous:
                if not isinstance(self.flag.function, core.render.Window):
                    awaitable = self.flag.function(*self.flag.arguments)
                else:
                    awaitable = self.flag.function
                res = await awaitable
                print(res)
                if res == "quit":
                    time.sleep(0.05)
                    self.finish("quit")
            else:
                self.flag.function()

    def render(self):
        core.Interface.render(self.mainloop)

    def _debug(self):
        return {
            "discovered": self.discovered,
            "position": self.position}


class Room(Stage):

    MinSegments = 2
    MaxSegments = 4
    GlobalStep = 16
    FloorHeight = 55
    HitBoxSize = 16
    BranchGenerateChance = [True, False]
    GoldenKeyChance = [True, False, False, False, False]

    def __init__(self, game):
        # Initalise
        super().__init__(game, handles.Room)
        self.hitboxes = {
            "left-exit": None,
            "right-exit": None,
            "golden-key": None
        }

    async def show(self):
        self._show()

        # Check for hints
        self.hint()

        if not self.discovered:
            # Generate Subwindow
            if random.choice(self.BranchGenerateChance):
                self.subwindow = Branch(self.game)
            else:
                self.subwindow = Room(self.game)
            self.subwindow.generate()
            self.discovered = time.strftime("%H:%M")

            # Increment Game Score
            self.game.scoring["score"] += int(1 * ((self.width / 128)) / 2)

    def generate(self):
        # Generate Room
        segments = random.randint(self.MinSegments, self.MaxSegments)
        self.scene = scene.Room(segments)
        self.width = 128 * segments

        # Create Exit Hitboxes
        self.hitboxes["left-exit"] = (0, self.HitBoxSize)
        self.hitboxes["right-exit"] = ((self.width) -
                                       self.HitBoxSize, (self.width))

        # Graphical Elements

        # Parallax
        self.parallax = Parallax([
            ParallaxLayer(self.scene.base, offset=0.3),
            ParallaxLayer(self.scene.background, offset=0.6),
            ParallaxLayer(self.scene.fixings, offset=0.7),
            ParallaxLayer(self.scene.foreground, offset=1)
        ], common.colour_strip(self.scene.base, y=64), self.GlobalStep)

        # Player
        self.player = Sprite(
            self.game.sprites["player"], (0, self.FloorHeight), self.GlobalStep)

        # Banner
        self.banner = Sprite(
            self.game.sprites["goldenkey-notify"], (64, 15), show=False)

        # Render
        self.elements = [self.parallax, self.player, self.banner]

        # Golden Key
        self.goldenkey = None
        if random.choice(self.GoldenKeyChance):
            self.goldenkey = items.GoldenKey(self.game.generate_keyvalue(5), self.game.sprites["goldenkey"],
                                             (128 + self.game.sprites["goldenkey"].width, self.FloorHeight), self.GlobalStep)
            self.elements.insert(1, self.goldenkey)
            self.hitboxes["golden-key"] = ((self.width / 2) - (
                self.HitBoxSize / 2), (self.width / 2) + (self.HitBoxSize / 2))
            self.game.golden_keys.put(self.goldenkey.hash)

        # Render
        self.mainloop = MainLoop(self.elements)

    def hint(self):
        _hit = False
        for hitbox in self.hitboxes.values():
            try:
                if hitbox[0] <= self.position <= hitbox[1]:
                    core.hw.Key.all(True)
                    _hit = True
                    break
            except TypeError:
                pass
        if not _hit:
            core.hw.Key.all(False)

    def debug(self):
        '''stats = {
            "width": self.width,
            "hitboxes": self.hitboxes,
            "DistanceFromMid": (self.width / 2) - self.position}'''
        # return stats.update(self._debug())
        return self._debug()


class Branch(Stage):

    AnimationSpeed = 0.7
    FloorHeight = 55
    PlayerSpeed = 8
    DoorGenerateChance = [True, True, True, True, False]
    TreasureRoomChance = [True, True, False, False, False]

    def __init__(self, game):
        # Initalise
        super().__init__(game, handles.Branch)
        self.doors = {
            "left": Door((21, 42), 32),
            "center": Door((42, 84), 64),
            "right": Door((84, 107), 96)}

    async def show(self):
        self._show()

        # Generate Subrooms
        if not self.discovered:
            for door in self.doors.values():
                if door.hook == self.finish:
                    # Approximate Door Position
                    self.position = door.spawnx
                    self.player.set_x(door.spawnx)
                elif door.hook is not None:
                    door.hook.generate()

            self.discovered = True
            self.game.scoring["depth_multiplier"] += 0.25

    def generate(self):
        # Generate Mapping
        self.doors[random.choice(list(self.doors.keys()))].hook = self.finish
        for key, door in zip(self.doors.keys(), self.doors.values()):
            if door.hook is None:
                if random.choice(self.DoorGenerateChance):
                    if random.choice(self.TreasureRoomChance) and not self.game.golden_keys.empty():
                        self.doors[key].hook = TreasureRoom(self.game)
                        self.doors[key].lock = self.game.golden_keys.get()
                    else:
                        self.doors[key].hook = Room(self.game)

        # Generate Branch
        self.scene = scene.Branch(
            [False if door.hook is None else True for door in self.doors.values()])

        # Graphical Elements

        # Background, Foreground & Backlight Animation
        self.background = Animation("image",
                                    self.scene.background_frames, speed=self.AnimationSpeed)
        self.foreground = Animation("image",
                                    self.scene.foreground_frames, speed=self.AnimationSpeed)
        self.backlight = Animation("backlight",
                                   self.scene.backlight_colours, speed=0.5)

        # Player
        self.player = Sprite(
            self.game.sprites["player"], (0, self.FloorHeight), self.PlayerSpeed)

        # Banner
        self.banner = Sprite(
            self.game.sprites["locked-notify"], (64, 15), show=False)

        # Render
        self.elements = [self.backlight, self.background,
                         self.player, self.foreground, self.banner]
        self.mainloop = MainLoop(self.elements)

    def debug(self):
        return self._debug()


class TreasureRoom(Stage):

    HitBoxSize = 10
    AnimationSpeed = 0.7
    PlayerSpeed = 8
    TreasureScoreValue = 40

    def __init__(self, game):
        super().__init__(game, handles.TreasureRoom)
        self.map = {
            "exit": (0, 0 + self.HitBoxSize),
            "treasure": (103, 103 + self.HitBoxSize)}

    async def show(self):
        self._show()

    def generate(self):
        # Generate Treasure
        self.scene = scene.Treasure()

        # Background Foreground & Backlight Animations
        self.background = Animation("image",
                                    self.scene.background_frames, speed=self.AnimationSpeed)
        self.foreground = Animation("image",
                                    self.scene.foreground_frames, speed=self.AnimationSpeed)
        self.backlight = Animation("backlight",
                                   self.scene.backlight_colours, speed=0.5)

        # Generate Heightmap
        self._generate_heightmap()

        # Player
        self.player = Sprite(
            self.game.sprites["player"], (0, self.heightmap[0]), self.PlayerSpeed)

        # Treasure
        self.treasure = Sprite(
            random.choice(self.game.sprites["treasures"]), (110, 45))

        # Render
        self.elements = [self.backlight, self.background, self.treasure,
                         self.player, self.foreground]
        self.mainloop = MainLoop(self.elements)

    def _generate_heightmap(self):
        image = self.scene.background_frames[0].copy().convert(
            "RGB").transpose(PIL.FLIP_TOP_BOTTOM)
        source = list(image.getdata())
        source = [source[x:x + 128] for x in range(0, len(source), 128)]
        self.heightmap = []
        for x in range(image.width):
            for y in range(image.height):
                if sum(list(source[y][x])) == 765:
                    self.heightmap.append(64 - y)
                    break

    def debug(self):
        return self._debug()


class Door:

    def __init__(self, hitbox: tuple, spawnx: int, hook: callable = None, lock: str = None):
        self.hitbox = hitbox
        self.spawnx = spawnx
        self.hook = hook
        self.lock = lock