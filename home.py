# I am the man who arranges the scripts
import core
import time

class Mainwindow(core.render.Window):

    def __init__(self):
        # HEADER
        self.template = f"{core.sys.PATH}core/resource/template/home.template"
        self.title1 = core.render.element.Text(core.Vector(3, 5), "TRasPi OS", colour=0, justify="L")
        self.title2 = core.render.element.Text(core.Vector(126, 5), time.strftime('%I:%M'), colour=0, justify="R")
        # BODY
        self.bttn1 = core.render.element.Text(core.Vector(64, 10), "Run Program")
        self.bttn2 = core.render.element.Text(core.Vector(64, 20), "Load Program")
        self.bttn3 = core.render.element.Text(core.Vector(64, 30), "System Settings")
        self.bttn4 = core.render.element.Text(core.Vector(64, 40), "Power Options")
        
