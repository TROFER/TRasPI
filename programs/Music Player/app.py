import core
from index import Index

class App(core.type.Application):
    name = "Music Player"

    class var(core.type.Config):
        rescan = True
        library = []
        volume = 75

    class const(core.type.Constant):
        directories = []
        screen_timeout = 30
        colour = core.sys.var.colour

    class player:
        sleeptimer = -1
        repeat = False

    class asset(core.asset.Pool):
        sleep_icon = core.asset.Image("icon-sleep")
        play_icon = core.asset.Image("player-play")
        pause_icon = core.asset.Image("player-pause")
        prev_icon = core.asset.Image("player-rewind")
        next_icon = core.asset.Image("player-next")
        repeat_icon = core.asset.Image("player-repeat")

    def constrain(n, start1, stop1, start2, stop2):
        return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

    def rescan(force=False):
        if App.var.rescan or force:
            App.var.library = Index.scan()
            if App.const.directories:
                for directory in App.const.directories:
                    App.var.library = App.var.library + Index.scan(path=directory)
            App.var.rescan = False