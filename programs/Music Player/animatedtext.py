import core
import time

class AnimatedText(core.element.Text):

    def __init__(self, pos, text, width):
        self.start = 0
        self.time = time.time()
        self._text = text
        if len(self._text) < width:
            self.end = len(self._text)
        else:
            self.end = width
        super().__init__(core.Vector(
            pos[0], pos[1]), self._text[self.start:self.end])

    def update(self):
        if time.time() - self.time > 1: #Speed
            if self.start < len(self._text):
                self.start += 1
            else:
                self.start = 0
            if self.end < len(self._text):
                self.end += 1
            else:
                self.end = 0
            self.time = time.time()
            self.text(self._text[self.start:self.end])
            print("Frame")
        print("Render")
        self.render()
