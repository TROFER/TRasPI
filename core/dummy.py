class Lcd:
    def __init__(self):
        self.buffer = [["[]" for y in range(128)] for x in range(64)]

    def setpixel(self, x, y, value):
        if value == 1:
            value = "#"
        else:
            value = "[]"
        self.buffer[x][y] = value

    def show(self):
        print("\n")
        print("\n".join((" ".join(row) for row in self.buffer)))
        print("\n")
