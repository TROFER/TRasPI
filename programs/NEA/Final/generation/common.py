def align(image, axis: str, alignment: str):
    alignments = {
        "x": {
            'c': 0 - (image.width / 2),
            'l': image.width,
            'r': 0 + image.width},
        "y": {
            'c': 0 - (image.height / 2),
            't': image.height,
            'b': 0 - image.height}}
    return int(alignments[axis.lower()][alignment.lower()])
