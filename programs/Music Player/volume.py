import os

class Volume:

    def __init__(self, step=5):
        self.volume = 75
        self.step = step
        self.set()

    def set(self):
        os.system(f"amixer set PCM {self.volume}%")

    def get(self):
        return f"{self.volume}%"

    def decrese(self):
        self.volume -= self.step
        self.set()

    def increse(self):
        self.volume += self.step
        self.set()
