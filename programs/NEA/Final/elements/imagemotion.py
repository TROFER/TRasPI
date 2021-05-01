# /elements/imagemotion.py

from PIL import Image


class ImageMotion:

    def __init__(self, image):
        self.stitch(image)
        self.x = 0
        self.y = 0
        self.crop()

    def copy(self):
        return self.image.copy()

    def move(self):
        if self.x != self.image.width / 2 and self.image.height / 2:
            self.x += 1
            self.y += 1
        else:
            self.x = 0
            self.y = 0
        self.crop()
    
    def crop(self):
        self.image = self.source.copy().crop((self.x, self.y, self.x + 128, self.y + 64))

    def stitch(self, image):
        stitch_x, stitch_y = image.image.width * 2, image.image.height * 2
        self.source = Image.new("1", (stitch_x, stitch_y))
        for x in range(0, stitch_x, image.image.width):
            for y in range(0, stitch_y, image.image.height):
                self.source.paste(image.image, (x, y))