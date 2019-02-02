from gfxhat import touch, lcd, backlight, fonts

'''
def set_backlight(r, g, b):
    backlight.set_all(r, g, b)
    backlight.show()
'''
def main_script(r,g,b):
    '''
    r = int(input("Enter Red Value MAX: 225 "))
    g = int(input("Enter Green Value MAX: 225 "))
    b = int(input("Enter Blue Value MAX: 225 "))
    '''
    backlight.set_all(r, g, b)
    backlight.show()
    print("Backlight Set...")
