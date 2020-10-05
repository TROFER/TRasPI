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

    class asset(core.asset.Pool):
        sleep_icon = core.asset.Image("icon-sleep")
        play_icon = core.asset.Image("player-play")
        pause_icon = core.asset.Image("player-pause")
        prev_icon = core.asset.Image("player-prev")
        next_icon = core.asset.Image("player-next")