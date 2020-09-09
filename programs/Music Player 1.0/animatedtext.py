import core
import time

class AnimatedText(core.element.Text):

    def __init__(self, pos, text, width, speed=0.5):
        self.buffer = [' ' for i in range(width)]
        self.width = width
        self.label = f"{text}{' '*width}"
        self.index = 0
        self.speed = speed
        self.time = time.time()
        self.state = True
        super().__init__(core.Vector(
            pos[0], pos[1]), "".join(self.buffer))

    def edit(self, text):
        if self.state:
            self.label = f"{text}{' '*self.width}"
            if self.index > len(self.label):
                self.toggle(True)
            self.index = 0

    def toggle(self, state=None):
        if state is None:
            self.state = not self.state
        else:
            self.state = state
        self.index = 0
        self.buffer = [' ' for i in range(self.width)]

    def update(self):
        if self.state:
            if time.time() - self.time > self.speed: #Speed
                self.buffer.pop(0)
                self.buffer.append(self.label[self.index])
                if self.index < len(self.label)-1:
                    self.index +=1
                else:
                    self.index = 0
                self.text("".join(self.buffer))
                self.time = time.time()
        self.render()
