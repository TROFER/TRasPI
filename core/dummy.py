
class lcd:
    def __init__(self):
        self.buffer = [["[]" for y in range(64)] for x in range(128)]


    def set_pixel(self, x, y, value):
        global lcd
        if value == 1:
            value = "#"
        else:
            value = "[]"
        self.buffer[x][y] = value

    def show(self):
        for x in range(128):
            print(" ".join(self.buffer[x][0:64]))
            print("\n")

a = lcd()
a.show()
