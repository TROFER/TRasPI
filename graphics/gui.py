import os
import core.log
import core.env
import graphics.menu

log = core.log.name("gui")

if core.env.ssh:
    #Text Terminal

    def cls():
        os.system("cls" if os.name == "nt" else "clear")

    output = print

    def menu():
        pass

    def draw(window):
        buffer = "\n/"
        buffer += "/".join((i.name for i in window.path))
        buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        if isinstance(window.current, graphics.menu.Page):
            buffer += window.current.draw()
            buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
            buffer += window.current.elements[window.cursor()].desc
            buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        elif isinstance(window.current, graphics.menu.Element):
            buffer += window.current.draw()
            buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
            buffer += window.current.desc
            buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        buffer += "MISC"
        buffer += "\n"+graphics.menu.LINE_BREAK+"\n"
        buffer += "BACK | ACCEPT | QUIT"

        #cls()
        print(buffer)

else:
    #LED Screen
    def cls():
        print("CLEARING")
    def output(*args):
        print("OUTPUT")
    def menu():
        print("MENU")
    def draw():
        print("DRAWING")
