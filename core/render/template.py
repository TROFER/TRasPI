from PIL import Image, ImageFont, ImageDraw

PATH = "/home/traspi"
background = Image.open(PATH+"core/menu.template").convert("P")
std_font = PATH+"fonts/font.ttf"
