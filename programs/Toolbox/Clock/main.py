import core
import time

class ProgramClock(core.render.Window):

    def __init__(self):
    
    def load(self):
        with open(f"{core.sys.PATH}programs/Toolbox/Clock/config.cfg") as config:
            self.config = json.load(config)
        self.clock, self.pwr_mode = self.config["clock_face"], self.config["pwr_mode"]

class Clock:

    @classmethod
    def time(cls):
        return time.strftime('%I:%M%p')
