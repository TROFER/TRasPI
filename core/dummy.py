WIDTH, HEIGHT = 128, 64

class lcd:

    buffer = [["#" for y in range(HEIGHT)] for x in range(WIDTH)]

    @classmethod
    def set_pixel(cls, x, y, value):
        if value == 1:
            value = "-"
        else:
            value = "#"
        cls.buffer[x][y] = value

    @classmethod
    def show(cls):
        print("\n\n\n////////////////////////////////////SHOW////////////////////////////////\n\n\n")
        for x in range(WIDTH):
            print(" ".join([cls.buffer[x][y] for y in range(HEIGHT)]))
            # print("\n\n\n/////////LINE/////////////\n\n\n")


class touch:

    def on(*args, **kwargs):
        pass
