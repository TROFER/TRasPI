# /game/handles.py


from windows.game import pausemenu


class Handle:

    def __init__(self, stage):
        self.stage = stage

    def esc(self):
        self.stage.flag = Flag(pausemenu.Main, arguments=[
            self.stage.game], asynchronous=True)

    def clamp(self, _min, data, _max):
        return max(_min, min(data, _max))


class Room(Handle):

    def interact(self):
        stage = self.stage

        hitbox = stage.hitboxes
        if hitbox["left-exit"][0] <= stage.position <= hitbox["left-exit"][1]:
            stage.flag = Flag(stage.finish)

        elif hitbox["right-exit"][0] <= stage.position <= hitbox["right-exit"][1]:
            stage.flag = Flag(stage.subwindow, asynchronous=True)

        elif stage.goldenkey and not stage.goldenkey.aquired:
            if hitbox["golden-key"][0] <= stage.position <= hitbox["golden-key"][1]:
                stage.goldenkey.show = False
                stage.goldenkey.aquired = True
                stage.game.scoring["golden_keys"].append(stage.goldenkey.hash)
                stage.hitboxes["golden-key"] = None
                stage.hint()
                stage.banner.peak(5)

    def right(self):
        stage = self.stage

        # Room
        if stage.position < stage.width - stage.player.sprite.width:
            stage.position += stage.GlobalStep

        # Parallax
        if 64 <= stage.position <= stage.width - 64:
            stage.parallax.increment()

        # Player
        stage.player.flip_forward()

        self._any()

    def left(self):
        stage = self.stage

        # Room
        if stage.position != 0:
            stage.position -= stage.GlobalStep

        # Parallax
        if 64 <= stage.position <= stage.width - 64:
            stage.parallax.decrement()

        # Player
        stage.player.flip_backward()

        self._any()

    def _any(self):
        stage = self.stage

        # Player Sprite
        if stage.position <= 64:
            stage.player.set_x(
                self.clamp(0, stage.position, 64 + (stage.player.sprite.width // 2)))
        elif stage.width - stage.position <= 64:
            stage.player.set_x(
                self.clamp(0, 128 - (stage.width - stage.position), 128 - stage.player.sprite.width))

        # Golden Key Sprite

        if stage.goldenkey:
            if abs((stage.width / 2) - stage.position) <= 128:
                stage.goldenkey.set_x(
                    int(64 + ((stage.width / 2) - stage.position)))

        # Check for hints
        stage.hint()


class Branch(Handle):

    def interact(self):
        stage = self.stage

        for door in stage.doors.values():
            if door.hitbox[0] <= stage.position <= door.hitbox[1]:
                if door.hook == stage.finish:
                    stage.flag = Flag(stage.finish)

                elif door.lock:
                    if door.lock in stage.game.scoring["golden_keys"]:
                        stage.flag = Flag(door.hook, asynchronous=True)
                    else:
                        stage.banner.peak(5)
                else:
                    stage.flag = Flag(door.hook, asynchronous=True)

    def right(self):
        # Player
        stage = self.stage
        if stage.position != 128:
            stage.position += stage.PlayerSpeed
            stage.player.increment()
        stage.player.flip_forward()

    def left(self):
        # Player
        stage = self.stage
        if stage.position != 0:
            stage.position -= stage.PlayerSpeed
            stage.player.decrement()
        stage.player.flip_backward()


class TreasureRoom(Handle):

    def interact(self):
        stage = self.stage

        if stage.map["exit"][0] <= stage.position <= stage.map["exit"][1]:
            stage.flag = Flag(stage.finish)

        elif stage.map["treasure"][0] <= stage.position <= stage.map["treasure"][1]:
            stage.game.scoring["score"] += stage.TreasureScoreValue
            stage.treasure.show = False
            stage.map.pop("treasure")

    def right(self):
        # Player
        stage = self.stage
        if stage.position != 128:
            stage.position += stage.PlayerSpeed
            stage.player.increment()
        stage.player.flip_forward()

        self._any()

    def left(self):
        # Player
        stage = self.stage
        if stage.position != 0:
            stage.position -= stage.PlayerSpeed
            stage.player.decrement()
        stage.player.flip_backward()

        self._any()

    def _any(self):
        stage = self.stage
        stage.player.set_y(stage.heightmap[stage.position])


class Flag:

    def __init__(self, function: callable, arguments: list = [], asynchronous: bool = False):
        self.function = function
        self.arguments = arguments
        self.asynchronous = asynchronous