def colour_strip(image, y):
    return [image.getpixel((x, y)) for x in range(0, image.width - 1)]
