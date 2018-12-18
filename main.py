# Core Modules
import core.log
import core.loader
import core.config
import core.execute

log = core.log.name("Main")

#Example
core.loader.load("programs.example")
core.execute.exec(core.loader.modules["example"])
