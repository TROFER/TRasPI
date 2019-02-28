from time import sleep
from sys import exit
from atexit import register
from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw

width, height = lcd.dimensions()

font = ImageFont.truetype(fonts.BitocraFull, 11)
#font = ImageFont.truetype(fonts.BitbuntuFull, 10)

image = Image.new('P', (width, height))

draw = ImageDraw.Draw(image)

null = input("Point A")
##########################################################Point A######################################
class MenuOption:
    def __init__(self, name, action, options=()):
        self.name = name
        self.action = action
        self.options = options
        self.size = font.getsize(name)
        self.width, self.height = self.size

    def trigger(self):
        self.action(*self.options)

def set_backlight(r, g, b):
    backlight.set_all(r, g, b)
    backlight.show()
    null = input("Point B")
    #########################################Point B#########################

menu_options = [
            MenuOption('Set BL Red', set_backlight, (255, 0, 0)),
            MenuOption('Set BL Green', set_backlight, (0, 255, 0)),
            MenuOption('Set BL Blue', set_backlight, (0, 0, 255)),
            MenuOption('Set BL Purple', set_backlight, (255, 0, 255)),
            MenuOption('Set BL White', set_backlight, (255, 255, 255)),
            MenuOption('Exit', exit, (0,))
        ]
null = input("Point C")
#####################################Point C##########################
current_menu_option = 1

trigger_action = False

def handler(ch, event):
    global current_menu_option, trigger_action
    if event != 'press':
        null = input("Point D")
        ###############################Point D#####################
        return
    if ch == 1:
        current_menu_option += 1
    if ch == 0:
        current_menu_option -= 1
    if ch == 4:
        trigger_action = True
    current_menu_option %= len(menu_options)
    null = input("Point E")
    ##################################Point E############################

for x in range(6):
    touch.set_led(x, 0)
    backlight.set_pixel(x, 255, 255, 255)
    null = input("Point F")
    ###############################Point F##################
    touch.on(x, handler)
    ##############################Point G#####################
    null = input("Point G")

backlight.show()

def cleanup():
    backlight.set_all(0, 0, 0)
    backlight.show()
    lcd.clear()
    lcd.show()
    #############################Point H#######################
    null = input("Point G")

register(cleanup)

try:
    while True:
        ###########################Point I##########################
        null = input("Point I")
        image.paste(0, (0, 0, width, height))
        offset_top = 0

        if trigger_action:
            menu_options[current_menu_option].trigger()
            trigger_action = False

        for index in range(len(menu_options)):
            if index == current_menu_option:
            #############################################Point J############################
                null = input("Point J")
                break
            offset_top += 12

        for index in range(len(menu_options)):
            x = 10
            y = (index * 12) + (height / 2) - 4 - offset_top
            option = menu_options[index]
            if index == current_menu_option:
                draw.rectangle(((x-2, y-1), (width, y+10)), 1)
            draw.text((x, y), option.name, 0 if index == current_menu_option else 1, font)
            ##########################################Point K###########################
            null = input("Point K")

        w, h = font.getsize('>')
        draw.text((0, (height - h) / 2), '>', 1, font)

        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                lcd.set_pixel(x, y, pixel)
                ###################################Point L############################
                print("Point L")

        lcd.show()
        ######################################################Point M############################
        print("Point M")

except KeyboardInterrupt:
    cleanup()
