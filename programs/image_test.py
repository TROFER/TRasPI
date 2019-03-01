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


lcd.clear()
lcd.show()


#atexit.register(clear)

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


    backlight.show()

    # Blit our image canvas to the LCD
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)

    lcd.show()
    time.sleep(1 / 30.0)
