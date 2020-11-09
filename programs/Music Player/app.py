import core

from player import main as player


class App(core.type.Application):
    name = "Music Player"

    class var(core.type.Config):
        rescan = True
        directories = []

    class const(core.type.Constant):
        screen_timeout = 30

    class asset(core.asset.Pool):
        sleep_icon = core.asset.Image("icon-sleep")
        stop_icon = core.asset.Image("player-stop")
        play_icon = core.asset.Image("player-play")
        pause_icon = core.asset.Image("player-pause")
        rewind_icon = core.asset.Image("player-rewind")
        next_icon = core.asset.Image("player-next")
        repeat_icon = core.asset.Image("player-repeat")
        battery_icon = core.asset.Image("icon-battery")
        splashscreen = core.asset.Image("splashscreen")

    def constrain(n: int, start1: int, stop1: int, start2: int, stop2: int):
        "Returns n as a proportion of the specified range"
        return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)

    def constrain_time(seconds: int):
        "Returns a timestamp"
        if seconds < 1:
            return "0:00"
        values = [seconds // 3600, (seconds % 3600) //
                  60, ((seconds % 3600) % 60)]
        if values[0] == 0:
            values.pop(0)
        return ":".join(["{0:0=2d}".format(int(value)) for value in values])

    async def hide():
        player.pause()
