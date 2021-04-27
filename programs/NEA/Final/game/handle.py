
from windows.game import pausemenu

class RoomHandle:

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
                room.banner.sprite = room.game.sprites["goldenkey-notify"]
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


class TransitionHandle:

    def __init__(self, transition):
        self.transition = transition

    def esc(self):
        self.transition.flag = Flag(pausemenu.Main, arguments=[
                                    self.transition.game], asynchronous=True)

    def interact(self):
        transition = self.transition

        for data in transition.mapping.values():
            if data[0][0] <= transition.position <= data[0][1]:
                if data[1] == transition.finish:
                    transition.flag = Flag(transition.finish)
                else:
                    transition.flag = Flag(data[1], asynchronous=True)

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


def clamp(_min, data, _max):
    return max(_min, min(data, _max))


class Flag:

    def __init__(self, function: callable, arguments: list = [], asynchronous: bool = False):
        self.function = function
        self.arguments = arguments
        self.asynchronous = asynchronous
