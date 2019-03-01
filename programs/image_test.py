#!/usr/bin/env python

import time
import sys
import atexit
from gfxhat import lcd, backlight, touch, fonts
from PIL import Image, ImageDraw, ImageFont
import yaml

print("""upinout.py
Micro Pinout! A tiny version of Pinout.xyz.
Ever wondered what your GPIO pins do? What their BCM/WiringPi numbers are?
Use - and + to navigate the header and find out!
To see alt modes, use ^ and v on the left.
Press Ctrl + C to exit.
""")

pinout = yaml.load(open("pinout.yaml").read())
src = Image.open("upinout.png").convert("P")

width, height = lcd.dimensions()

font = ImageFont.truetype(fonts.BitocraFull, 11)

current_pin = 0
current_page = 0
running = True

backlight.set_all(255, 255, 255)
backlight.show()


def draw_cursor(image, x, y, direction):
    y = y if direction else y + 2

    image.putpixel((x + 2, y), 1)

    y = y + 1 if direction else y - 1
    for p in range(3):
        image.putpixel((x + 1 + p, y), 1)

    y = y + 1 if direction else y - 1
    for p in range(5):
        image.putpixel((x + p, y), 1)


def clear():
    lcd.clear()
    lcd.show()
    backlight.set_all(0, 0, 0)
    backlight.show()

atexit.register(clear)

while running:
    img = src.copy()
    draw = ImageDraw.Draw(img)

    if (current_pin + 1) % 2 == 0:
        offset_x = ((current_pin + 1) // 2) * 6
        offset_y = 9
        direction = 0
    else:
        offset_x = ((current_pin + 2) // 2) * 6
        offset_y = 25
        direction = 1

    draw_cursor(img, offset_x - 2, offset_y, direction)

    backlight.show()

    # Blit our image canvas to the LCD
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)

    lcd.show()
    time.sleep(1 / 30.0)
