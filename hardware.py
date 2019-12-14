from gfxhat import backlight, touch, lcd
# --------------------------------Hardware Control------------------------------#
def touch_led(leds=None, value=0):
    if leds is None:
        leds = [0, 1, 2, 3, 4, 5]
    for led in leds:
        touch.set_led(led, value)


def backlight_fill(colours=(225, 225, 225), percent=70):
    _colours = [colour / 100 for colour in colours]
    backlight.set_all(round(_colours[0] * percent), round(_colours[1] * percent), round(_colours[2] * percent))
    backlight.show()


def backlight_gradient(colours):
    for led in range(5):
        _colours = [int(hex_colour, 16) for hex_colour in [colours[led][i:i + 2] for i in range(0, 6, 2)]]
        backlight.set_pixel(led, _colours[0], _colours[1], _colours[2])
    backlight.show()


def clear_screen():
    lcd.clear(), lcd.show()
# -----------------------------End Hardware Control-----------------------------#
