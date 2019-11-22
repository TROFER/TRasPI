from sys import path
from gfxhat import touch, lcd, backlight
path.append("/home/traspi/system_assets")
import image, menu, backlight_control, num_sel, msg_check
from time import sleep

def torch():
    # Handler
    def handler_t(ch, event):
        if event == "press":
            global execute, torch_state
            if ch == 2:
                execute = False
            elif ch == 4:
                torch_state = not torch_state
                if torch_state:
                    backlight_control.linear(100)
                    image.main(f"/home/traspi/programs/torch/{torch_state}.png", False)
                    led_control(1)
                elif not torch_state:
                    backlight_control.linear(70)
                    image.main(f"/home/traspi/programs/torch/{torch_state}.png", False)
                    led_control(0)

    # Led Control
    def led_control(state):
        for button in range(6):
            touch.set_led(button, state)

    global execute, torch_state
    execute, torch_state = True, True
    touch.on(2, handler_t), touch.on(4, handler_t)
    backlight_control.linear(100), image.main(f"/home/traspi/programs/torch/{torch_state}.png", False), led_control(1)
    while execute:
        sleep(0.01)
    backlight_control.linear(70), lcd.clear(), lcd.show(), led_control(0)


def rgb():
    def rgb_handler(ch, event):
        if event == "press" and ch == 2:
            global execute
            execute = False
    global execute
    execute = True
    touch.on(2, rgb_handler)
    while execute:
        backlight_control.linear(70)
        r = num_sel.main("Enter Red Value")
        g = num_sel.main("Enter Green Value")
        b = num_sel.main("Enter Blue Value")
        backlight.set_all(r, g, b)
        backlight.show()
        execute = msg_check.main("Re Run?")


def emergency():
    def handler_e(ch, event):
        if event == "press" and ch == 2:
            global execute
            execute = False
    global execute
    execute = True
    touch.on(2, handler_e)
    while execute:
        backlight.set_all(225, 0, 0), backlight.show()
        sleep(0.1)
        backlight.set_all(225, 225, 225), backlight.show()
        sleep(0.1)
        backlight.set_all(0, 0, 225), backlight.show()
        sleep(0.1)

def main():
    menu_map = {1: torch, 2: rgb, 3: emergency, False: quit}
    while True:
        backlight_control.linear(70)
        command = menu_map[core.menu([1, 2, 3],["Torch", "RGB Mode", "Em Mode"])]
        command()
        lcd.clear(), lcd.show()

main()
