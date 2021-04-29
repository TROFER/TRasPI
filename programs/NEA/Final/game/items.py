from elements.game import sprite

class GoldenKey(sprite.Sprite):

    def __init__(self, hash, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash = hash
        self.aquired = False