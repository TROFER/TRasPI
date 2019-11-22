from time import sleep, strftime
from gfxhat import lcd, backlight, touch
from PIL import Image, ImageDraw, ImageFont
from os import getpid, kill
import signal
import timeit


def setup():
    with open("clock.cache", 'w') as cache:
        cache.write(str(getpid()))
    backlight_control(70)
    touch.set_led(2, 1)
    for i in range(6):
        touch.on(i, handler)


def backlight_control(value):
    backlight.set_all(round(2.25 * value), round(2.25 * value), round(2.25 * value))
    backlight.show()


def get_time():
    return strftime('%I:%M:%S')


def handler(ch, event):
    backlight_control(70)
    if ch == 2:
        with open("clock.cache") as cache:
            pid = cache.read()
        lcd.clear(), lcd.show(), backlight_control(0), touch.set_led(2, 0)
        kill(int(pid), signal.SIGKILL)


def main():
    w, h = 128, 64
    setup()
    while True:
        render(w, h)
        sleep(60 - int(get_time()[6:8]))
        backlight_control(30)


def render(w, h):
    clock = Image.new('P', (w, h))
    draw = ImageDraw.Draw(clock)
    font = ImageFont.truetype('../fonts/font.ttf', 50)
    time = get_time()[0:5]
    font_w, font_h = font.getsize(time)
    pos_x, pos_y = (128 - font_w) // 2, (64 - font_h) // 2
    draw.text((pos_x, pos_y), get_time()[0:5], 1, font)
    update_display(clock)



def update_display(clock):
    for x in range(128):
        for y in range(64):
            lcd.set_pixel(x, y, clock.getpixel((x, y)))
    lcd.show()
        

main()
