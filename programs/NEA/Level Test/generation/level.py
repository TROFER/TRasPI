import random


class Level:

    Constraints = {"min" : 3, "max" : 6}

    def __init__(self):
        self.depth = random.randint(self.Constraints["min"], self.Constraints["max"])
        self.generate()

    def generate(self):
        self.level = 
        for layer_number in range(self.depth):



level = [
    [[], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], [], []]
]