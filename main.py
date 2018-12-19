# Core Modules
import core.log
import core.loader
import core.config
import core.execute
import util.misc

log = core.log.name("Main")
core.config.load("core", "cfg")
core.log.level(core.config.cfg["core"]["log level"])

util.misc.cls()

#Example
core.loader.load("programs.example")
core.execute.exec(core.loader.modules["example"])
util.misc.cls()

print("END MAIN")
