from gfxhat import lcd, backlight, touch
from PIL import Image, ImageDraw, ImageFont
from time import time

def image(file):
    from gfxhat import lcd
    from PIL import Image, ImageDraw, ImageFont
    width, height = lcd.dimensions()
    image_new= Image.open(file).convert("P")
    draw_image(file, width, height, image_new)
    return

def draw_image(file, width, height, image_new):
    ########Get old######
    image_old= Image.open("05_keycard.png")
    ########Render#######
    for x in range(width):
        for y in range(height):
            if image_new.getpixel((x,y)) != image_old.getpixel((x,y)):
                pixel = image_new.getpixel((x,y))
                lcd.set_pixel(x, y, pixel)
            else:
                continue
    ########Render#######
    image_new.save("cache_old.png")
    lcd.show()
    return


backlight.set_all(200,200,200)
backlight.show()

a = time()
image("05_keycard.png")
lcd.show()
print (time() -a)
b = time()
image("no_conection.png")
print (time() -b)
