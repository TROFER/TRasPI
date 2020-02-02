import core

class AnimatedText(core.element.Text):

    def __init__(self, pos, text, width):
        self.begin = 0
        self.time = time.time()
        self.text = text
        if len(self.text) < width:
            self.end = len(self.text)
        else:
            self.end = width
        super().__init__(core.Vector(
            pos[0], pos[1]), self.text[self.start:self.end])

    def update(self):
        if time.time() - self.time > 1:  # Speed
            if self.start < len(self.text):
                self.start += 1
            else:
                self.start = 0
            if self.end < len(self.text):
                self.start += 1
            else:
                self.end = 0
        self.render()
