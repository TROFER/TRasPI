import importlib
import time
import os

try:
    import core
except ImportError as e:
    raise OSError("FAILURE TO LOAD CORE!") from e
try:
    module = importlib.import_module("home")
except Exception as e:
    raise OSError("FAILURE TO BOOT!") from e

if not hasattr(module, "main"):
    msg = "FAIL! '{}' has no 'main'!".format(module.__name__)
    raise OSError(msg)

if not isinstance(module.main, core.render.Window):
    msg = "FAIL! {}.main <{} '{}'> is not an instance of 'core.render.Window'!".format(module.__name__, type(module.main).__name__, module.main)
    raise OSError(msg)

try:
    module.main.show()
    core.render.loop()
except Exception as e:
    raise OSError from e

# time.sleep(5)
# os.system("halt") # Turn off the device
