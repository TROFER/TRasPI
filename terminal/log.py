class Log:

    def __init__(self, name="Log", level=0):
        self.name, self.level = name, level

    def __repr__(self):
        return "{} - {}".format(self.name, self.level)
