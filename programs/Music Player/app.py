import core
import player

class App(core.type.Application):
    name = "Music Player"

    class var(core.type.Config):
        rescan = False

    class const(core.type.Constant):
        screen_timeout = 30

    class asset(core.asset.Pool):
        sleep_icon = core.asset.Image("icon-sleep")
        play_icon = core.asset.Image("player-play")
        pause_icon = core.asset.Image("player-pause")
        rewind_icon = core.asset.Image("player-rewind")
        next_icon = core.asset.Image("player-next")
        repeat_icon = core.asset.Image("player-repeat")

    def constrain(n, start1, stop1, start2, stop2):
        return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

    async def hide():
        player.stop()