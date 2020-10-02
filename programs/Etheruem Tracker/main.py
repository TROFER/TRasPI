import core
import urllib.request
import json

class Main(core.render.Window):

    def __init__(self):
        self.elements = []

    
    def getprice(self):
        with open(f"{core.sys.const.path}user/coinapi.txt") as key:
            key = key.read
        return 
