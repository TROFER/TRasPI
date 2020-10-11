import core.error
import core.error.attributes
if core.error.attributes.SysConstant.process:
    from core.vector import Vector
    import core.sys
    import core.render
    import core.input

    from core.sys import log
    from core.render import element

    import core.application

    import core.type
    from core.interface import Interface, interface

    import core.std

    log.core.info("System:\n\tPlatform: %s\n\tPath: '%s'\n\tSize: %d, %d\n\tPipeline: %s", core.sys.const.platform, core.sys.const.path, core.sys.const.width, core.sys.const.height, core.sys.const.pipeline)
    log.core.info("Configuration:\n\tName: %s\n\tBrightness: %d\n\tColour: %d", core.sys.var.name, core.sys.var.brightness, core.sys.var.colour)