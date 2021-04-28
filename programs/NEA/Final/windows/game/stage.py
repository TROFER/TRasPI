import asyncio
import random
import time

import core
from app import App
from elements.game import Animation, MainLoop, Parallax, ParallaxLayer, Sprite
from generation import scene
from PIL import Image as PIL

from game import common, keyboard, handles


class Stage:

    InputRateLimit = 1

    def __init__(self, game, handle):
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
                if res == "quit":
                    self.finish("quit")
            else:
                self.flag.function()
    
    def render(self):
        core.Interface.render(self.mainloop)
    
    def _debug():
        return {
            "discovered" : self.discovered,
            "position" : self.position}


class Room(Stage, core.render.Window):

    MinSegments = 2
    MaxSegments = 4
    GlobalStep = 16
    FloorHeight = 55
    HitBoxSize = 16
    BranchGenerateChance = [True, False]
    GoldenKeyChance = [True]  # CHANGE ME

    def __init__(self, game):
        # Initalise
        super(core.render.Window).__init__()
        super(Stage).__init__(game, handles.Room)

        self.hitboxes = {
            "left-exit": None,
            "right-exit": None,
            "golden-key": None
        }

    async def show(self):
        super(Stage)._show()

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
            self.game.sprites["goldenkey-notify"], (64, 20), show=False)

        # Render
        self.elements = [self.parallax, self.player, self.banner]

        # Golden Key
        self.goldenkey = None
        if random.choice(self.GoldenKeyChance):
            self.goldenkey = Sprite(self.game.sprites["goldenkey"],
                                    (128 + self.game.sprites["goldenkey"].width, self.FloorHeight), self.GlobalStep)
            self.elements.insert(1, self.goldenkey)
            self.hitboxes["golden-key"] = ((self.width / 2) - (self.HitBoxSize / 2),
                                           (self.width / 2) + (self.HitBoxSize / 2))
            self.game.golden_keys.put(self.game.generate_keyvalue(5))

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
        stats = {
            "width": self.width,
            "hitboxes": self.hitboxes,
            "DistanceFromMid": (self.width / 2) - self.position}
        return super(Stage)._debug().update(stats)
        


class Branch(Stage, core.render.Window):

    AnimationSpeed = 0.7
    FloorHeight = 55
    PlayerSpeed = 8
    DoorGenerateSeed = [True, True, True, True, False] # 3/5 Chance to get an addional door

    def __init__(self, game):
        # Initalise
        super(core.render.Window).__init__()
        super(Stage).__init__(game, handles.Branch)
        
        self.mapping = {
            "left-exit": [(21, 42), None, 32],
            "center-exit": [(42, 84), None, 64],
            "right-exit": [(84, 107), None, 96]
        }

    async def show(self):
        super(Stage)._show()

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
            self.game.scoring["depth_multiplier"] += 0.25

    def generate(self):
        # Generate Mapping
        self.mapping[random.choice(list(self.mapping.keys()))][1] = self.finish
        for key, data in zip(self.mapping.keys(), self.mapping.values()):
            if data[1] is None:
                if random.choice(self.DoorGenerateSeed):
                    self.mapping[key][1] = Room(self.game)

        # Generate Branch
        self.scene = scene.Branch(
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
        self.player = Sprite(
            self.game.sprites["player"], (0, self.FloorHeight), self.PlayerSpeed)

        # Render
        self.elements = [self.backlight, self.background,
                         self.player, self.foreground]
        self.mainloop = MainLoop(self.elements)

    def debug(self):
        super(Stage)._debug()


class TreasureRoom(core.render.Window):

    HitBoxSize = 10

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.handle = handle.TreasureRoomHandle(self)
        self.flag = None
        self.position = 0
        self.mapping = {
            "exit": [(0, 0 + self.HitBoxSize)]
        }

    async def show(self):
        # Reset
        self.flag = None

        # Set Keybindings
        keyboard.Hotkey("esc", self.handle.esc)
        keyboard.Hotkey("e", self.handle.interact,
                        rate_limit=self.InputRateLimit)
        keyboard.Hotkey("a", self.handle.left, rate_limit=self.InputRateLimit)
        keyboard.Hotkey("d", self.handle.right, rate_limit=self.InputRateLimit)

        # Update Game Active Window
        self.game.active_window = self

    def generate(self):
        # Generate Treasure
        self.scene = scene.TreasureRoom()

        # Background Foreground & Backlight Animations
        self.background = Animation("image",
                                    self.scene.background_frames, speed=self.AnimationSpeed)
        self.foreground = Animation("image",
                                    self.scene.foreground_frames, speed=self.AnimationSpeed)
        self.backlight = Animation("backlight",
                                   self.scene.backlight_colours, speed=0.5)
