import sys

def colour_strip(image, y):
    image = image.copy().convert("RGB")
    return [image.getpixel((x, y)) for x in range(0, image.width - 1)]