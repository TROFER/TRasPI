
from windows.game import pausemenu

class Room:

    def __init__(self, room):
        self.room = room

    def esc(self):
        self.room.flag = Flag(pausemenu.Main, arguments=[
                              self.room.game], asynchronous=True)

    def interact(self):
        room = self.room

        hitbox = room.hitboxes 
        if hitbox["left-exit"][0] <= room.position <= hitbox["left-exit"][1]:
            room.flag = Flag(room.finish)

        elif hitbox["right-exit"][0] <= room.position <= hitbox["right-exit"][1]:
            room.flag = Flag(room.subwindow, asynchronous=True)
        
        elif room.goldenkey:
            if hitbox["golden-key"][0] <= room.position <= hitbox["golden-key"][1]:
                room.goldenkey.show = False
                room.game.scoring["golden_keys"] += 1
                room.hitboxes["golden-key"] = None
                room.hint()
                room.banner.peak(5)

    def right(self):
        room = self.room

        # Room
        if room.position < room.width - room.player.sprite.width:
            room.position += room.GlobalStep

        # Parallax
        if 64 <= room.position <= room.width - 64:
            room.parallax.increment()

        # Player
        room.player.flip_forward()

        self._any()

    def left(self):
        room = self.room

        # Room
        if room.position != 0:
            room.position -= room.GlobalStep

        # Parallax
        if 64 <= room.position <= room.width - 64:
            room.parallax.decrement()

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

        # Golden Key Sprite

        if room.goldenkey:
            if abs((room.width / 2) - room.position) <= 128:
                room.goldenkey.set_position(
                    int(64 + ((room.width / 2) - room.position)))

        # Check for hints
        room.hint()


class Branch:

    def __init__(self, branch):
        self.branch = branch

    def esc(self):
        self.branch.flag = Flag(pausemenu.Main, arguments=[
                                    self.branch.game], asynchronous=True)

    def interact(self):
        branch = self.branch

        for data in branch.mapping.values():
            if data[0][0] <= branch.position <= data[0][1]:
                if data[1] == branch.finish:
                    branch.flag = Flag(branch.finish)
                else:
                    branch.flag = Flag(data[1], asynchronous=True)

    def right(self):
        # Player

        branch = self.branch
        if branch.position != 128:
            branch.position += branch.PlayerSpeed
            branch.player.increment()

        branch.player.flip_forward()

    def left(self):
        # Player

        branch = self.branch
        if branch.position != 0:
            branch.position -= branch.PlayerSpeed
            branch.player.decrement()

        branch.player.flip_backward()


def clamp(_min, data, _max):
    return max(_min, min(data, _max))


class Flag:

    def __init__(self, function: callable, arguments: list = [], asynchronous: bool = False):
        self.function = function
        self.arguments = arguments
        self.asynchronous = asynchronous
