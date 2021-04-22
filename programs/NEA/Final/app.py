import core

class App(core.type.Application):
    name = "Dungeon Runner"

    class var(core.type.Config):
        playerskin = None

    class const(core.type.Constant):
        debug = False

    class asset(core.type.Pool):
        ts_template = core.asset.Template("ts_template")
        ts_keyboard = core.asset.Image("fs_keyboard")
        ts_title = core.asset.Image("ts_title")
        ts_cursor = core.asset.Image("ts_cursor")
        rs_gameover = core.asset.Image("rs_gameover")
        pm_paused = core.asset.Image("pm_paused")

main = App