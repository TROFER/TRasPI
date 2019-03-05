#!/usr/bin/env python
from time import sleep
import sys
import atexit
from gfxhat import lcd, backlight
from PIL import Image, ImageDraw, ImageFont
from graphics import cleanup

width, height = lcd.dimensions()
backlight.set_all(255, 255, 255)
backlight.show()

def load():
    while True:
        try:
            file = input("Enter full directory path: ")
        except KeyboardInterrupt:
            quit()
        try:
            src = Image.open("/home/os/graphics/global images/05_keycard.png").convert("P")
            display(src)
            return
        except IOError:
            print("File not found")


def display(src):
    width, height = lcd.dimensions()
    running = True
    backlight.set_all(255, 255, 255)
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


        backlight.show()

        # Blit our image canvas to the LCD
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                lcd.set_pixel(x, y, pixel)

        lcd.show()
        time.sleep(1 / 30.0)
        return

def main():
    cleanup()
    print("Basic image loading program\nAll images must be 128x64 black and white only\nType !load to begin loading images")
    while True:
        try:
            option = input("").lower().replace(" ","")
        except KeyboardInterrupt:
            quit()
        if option == "!load":
            load()
