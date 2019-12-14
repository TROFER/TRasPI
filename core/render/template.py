from PIL import Image, ImageFont, ImageDraw
from core.sys import PATH

background = Image.open(PATH+"core/assets/menu.template").convert("P")
std_font = PATH+"fonts/font.ttf"
