import os
import core.log
import core.env
import graphics.menu

log = core.log.name("gui")

misc_buffer = ""

if core.env.ssh:
    #Text Terminal

    def cls():
        os.system("cls" if os.name == "nt" else "clear")

    def output(*args):
        global misc_buffer
        for i in args:
            misc_buffer += str(i)

    def draw(window):
        global misc_buffer
        buffer = "\n/"
        buffer += "/".join((i.name for i in window.path))
        buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        buffer += window.buffer
        buffer += misc_buffer
        misc_buffer = ""
        buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        buffer += "A: BACK | D: ACCEPT | E: QUIT"

        cls()
        print(buffer)

else:
    #LED Screen
    def cls():
        print("CLEARING")
    def output(*args):
        print("OUTPUT")
    def draw():
        print("DRAWING")
