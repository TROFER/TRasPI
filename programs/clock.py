import time
import signal
from time import gmtime, strftime
from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw

print("Use ctrl+c To Quit")
try:
    while True:
        led_states = [False for _ in range(6)]

        width, height = lcd.dimensions()

        image = Image.new('P', (width, height))

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(fonts.clock, 20)

        text = strftime("%H:%M", gmtime())

        w, h = font.getsize(text)

        x = (width - w) // 2
        y = (height - h) // 2

        draw.text((x, y), text, 1, font)

        def handler(ch, event):
            if event == 'press':
                led_states[ch] = not led_states[ch]
                touch.set_led(ch, led_states[ch])
                if led_states[ch]:
                    backlight.set_pixel(ch, 0, 255, 255)
                else:
                    backlight.set_pixel(ch, 0, 255, 0)
                backlight.show()

        for x in range(6):
            touch.set_led(x, 1)
            time.sleep(0.1)
            touch.set_led(x, 0)

        for x in range(6):
            backlight.set_pixel(x, 0, 255, 0)
            touch.on(x, handler)

        backlight.show()

        for x in range(128):
            for y in range(64):
                pixel = image.getpixel((x, y))
                lcd.set_pixel(x, y, pixel)


        lcd.show()

        try:
            signal.pause()
        except KeyboardInterrupt:
            for x in range(6):
                backlight.set_pixel(x, 0, 0, 0)
                touch.set_led(x, 0)
            backlight.show()
            lcd.clear()
            lcd.show()
            time.sleep(1)

except KeyboardInterrupt:
    bob + 5
    quit()
