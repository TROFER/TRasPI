from typing import Type
from ..error.attributes import Config

class Setting:

    def __init__(self, attr: str, name: str=None, data: type=None, **data_type):
        self.attr, self.name = attr, name or attr
        self.data_type = data
        self.data_kwargs = data_type
        self.categories = []