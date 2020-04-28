import json
import os

from core.asset.image import Image


class Program:

    def __init__(self, location, icon=None):
        self.location, self.icon = location, icon

    def remove(self):
        os.rmdir(self.location)

    def description(self):
        try:
            with open(f"{SysConstant.path}programs/{target}/README.txt", 'r') as description:
                return description.read()
        except FileNotFoundError:
            return None

    def config(self, new_config=None):
        if config is None:
            try:
                with open(f"{SysConstant.path}programs/{self.name}/config.json", 'r') as config:
                    return json.load(config)
            except FileNotFoundError:
                return None
        else:
            with open(f"{SysConstant.path}programs/{self.name}/config.json", 'w') as config:
                json.dump(new_config, config)
