import gfxhat

'''
def set_backlight(r, g, b):
    backlight.set_all(r, g, b)
    backlight.show()
'''

while True:
    r = int(input("Enter Red Value MAX: 225 "))
    g = int(input("Enter Green Value MAX: 225 "))
    b = int(input("Enter Blue Value MAX: 225 "))
    set_backlight(r,g,b)
    print("Backlight Set...")
