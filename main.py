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

core.loader.load("programs.example")
# core.execute.exec(core.loader.modules["example"])

#---Functions------------------------------------------------------------------#

def get_programs_run(self):
    self.actions = [graphics.menu.Action(window, p, "run", p.title(), "Run: "+p) for p in core.loader.modules]

def action_callback(action):
    if action.type == "run":
        core.execute.exec(core.loader.modules[action.func])
    elif action.type == "load":
        core.loader.load("programs."+action.func)

#---Setup----------------------------------------------------------------------#

count = 0

window = graphics.menu.Window(action_callback)
graphics.menu.Page(window, "Main",
graphics.menu.Action(window, "programs", "show", "Programs", "Run and Load Programs"),
graphics.menu.Action(window, "options", "show", "Options", "Edit Program Options"),
graphics.menu.Action(window, "test", "elmt", "Test", "Test Element"))

graphics.menu.Page(window, "programs",
graphics.menu.Action(window, "programs_run", "show", "Run", "Run Programs"),
graphics.menu.Action(window, "programs_load", "show", "Load", "Load Programs"))

graphics.menu.Page(window, "programs_run",
load=get_programs_run)

graphics.menu.Page(window, "options")

graphics.menu.Element(window, "test", "hello world how are you today?\nthank you i am doing fine!",
load=lambda self: self("\n".join([str(i) for i in range(count)])))

window.set_page("Main")

#---Main-----------------------------------------------------------------------#

x = ""
while x != "e":
    count += 1
    window.update()
    graphics.gui.draw(window)
    x = input().lower()
    if x == "s":
        window.move(1)
    elif x == "w":
        window.move(-1)
    elif x == "d":
        window.select()
    elif x == "a":
        window.back()

print("END MAIN")
