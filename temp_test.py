import core
import core.sys

print(core.sys.PATH)

info = core.std.Error("Info")
numpad = core.std.Numpad(2, 8000)
menu = core.std.Menu(info=info, num=numpad)



menu.show()

core.render.loop()
