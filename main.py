#---Core-----------------------------------------------------------------------#

# Core Modules
import core.log
import core.loader
import core.config
import core.execute
import core.env

#Core Setup
log = core.log.name("Main")
core.config.load("core", "cfg")
core.log.level(core.config.cfg["core"]["log level"])
if "--ssh" not in core.env.argv:
    core.env.ssh = False

#Core Logging Setup
log.info("-=Core Setup=-")
log.info("Log Level: ", core.log.LEVEL)
log.info("SSH: ", core.env.ssh)

core.env.ssh = True # TEMP

#---Graphics-------------------------------------------------------------------#

#Graphics Modules
import graphics.gui
import graphics.menu

#Grpahics Setup
core.env.window = graphics.menu.Window()

#Grpahics Logging Setup
log.info("-=Graphics Setup=-")

#---Complete-------------------------------------------------------------------#

#Logging Setup Complete
log.info("-=Setup Complete=-\n")

#---Example--------------------------------------------------------------------#

# core.loader.load("programs.example")
# core.execute.exec(core.loader.modules["example"])
# util.misc.cls()

#---Functions------------------------------------------------------------------#

#---Setup----------------------------------------------------------------------#

def action_callback(action):
    if action.type == "back":
        action.parent.back()
    elif action.type == "show":
        action.parent.forward(action.parent.pages[action.string])
    elif action.type == "run":
        core.execute.exec(core.loader.modules[action.string])
    elif action.type == "load":
        core.loader.load("programs."+action.string)

window = graphics.menu.Window(action_callback)
graphics.menu.Page(window, "Main",
graphics.menu.Element("Programs", "Run and Load Programs", graphics.menu.Action(window, "programs_run", "show", "Run"), graphics.menu.Action(window, "programs_load", "show", "Load")),
graphics.menu.Element("Options", "desc2", graphics.menu.Action(window, "2", "run", "r1"), graphics.menu.Action(window, "2", "back", "r2")))

graphics.menu.Page(window, "programs_run", *[graphics.menu.Element(p, "Program", graphics.menu.Action(window, p, "run", "Run"), graphics.menu.Action(window, "back", "back", "Back")) for p in core.loader.modules])

window.set_page("Main")

#---Main-----------------------------------------------------------------------#

graphics.gui.draw(window)

x = ""
while x != "e":
    x = input().lower()
    if x == "s":
        window.move(1)
    elif x == "w":
        window.move(-1)
    elif x == "d":
        window.select()
    elif x == "a":
        window.back()
    graphics.gui.draw(window)

print("END MAIN")
