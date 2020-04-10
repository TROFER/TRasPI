class Line(Primative):

    def __init__(self, pos1, pos2, colour=0, width=1, joint=None):
        super().__init__()
        self.colour, self.width, self.joint = colour, width, joint
        self.pos1, self.pos2 = pos1, pos2

    def copy(self):
        return self.pos1, self.pos2, self.colour, self.width

    def render(self):
        ImageDraw.line([*self.pos1, *self.pos2],
                       self.colour, self.width, self.joint)
