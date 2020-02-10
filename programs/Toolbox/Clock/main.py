import core
import time

class ProgramClock(core.render.Window):

    def __init__(self):
        self.load()
        
    def load(cls):
        with open(f"{core.sys.PATH}programs/Toolbox/Clock/config.cfg") as config:
            self.config = json.load(config)

class Clock:

    @classmethod
    def time(cls):
        return time.strftime('%I:%M%p')
