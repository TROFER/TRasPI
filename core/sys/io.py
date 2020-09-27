# import asyncio
from ..interface import Interface
from ..error.attributes import Config, SysConstant
from typing import Union, Type, IO
import pickle
import os
# import functools

class AIOFile(IO):

    def __init__(self, file: Union[str, bytes, int], *args, **kwargs):
        self.__file = None
        self.__args = (file, args, kwargs)

    async def __aenter__(self) -> IO:
        self.__file = await Interface.process(open, self.__args[0], *self.__args[1], **self.__args[2])
        return self.__file

    def __aexit__(self, *args):
        return Interface.process(self.__file.close)

    def __enter__(self) -> IO:
        self.__file = open(self.__args[0], *self.__args[1], **self.__args[2])
        return self.__file

    def __exit__(self, *args):
        return self.__file.close()

    def __getattribute__(self, name: str):
        if name.startswith("_"):
            return super().__getattribute__(name)
        if self.__file is None:
            raise IOError("File not Open")
        return self.__file.__getattribute__(name)
    def __setattr__(self, name: str, value):
        if name.startswith("_"):
            return super().__setattr__(name, value)
        if self.__file is None:
            raise IOError("File not Open")
        return self.__file.__setattr__(name, value)

class ConfigCache:

    DIR = SysConstant.path+"{}resource/program/"
    MANAGER = DIR+"vcm"
    OBJECT = DIR+"{}.vcm"

    @classmethod
    def read(cls, path: str, config: Type[Config]) -> Type[Config]:
        try:
            with AIOFile(cls.MANAGER.format(path), "r") as file_manager:
                files = file_manager.readlines()
            data = {}
            for key in files:
                key = key.strip()
                with AIOFile(cls.OBJECT.format(path, key), "rb") as file:
                    data[key] = pickle.load(file)
            if data:
                config.__setstate__(data)
        except (FileNotFoundError, EOFError) as e:    pass
        return config

    @classmethod
    def write(cls, path: str, config: Type[Config]) -> Type[Config]:
        try:
            with AIOFile(cls.MANAGER.format(path), "w") as file_manager:
                for key, value in config.__getstate__().items():
                    with AIOFile(cls.OBJECT.format(path, key), "wb") as file:
                        pickle.dump(value[0], file)
                    file_manager.write(f"{key}\n")
        except FileNotFoundError:
            os.makedirs(cls.DIR.format(path))
            cls.write(path, config)
        return config

# def _gen_map(dictionary):
#     return {word: chr(value) for value, word in enumerate(dictionary, start=129)}

# class Encrypt:

#     @classmethod
#     def otk(cls, string):  # Encrypts data using a one-time-key
#         key = []
#         output = []
#         for char in string:
#             val = random.randint(0, 30)
#             output.append(chr(ord(char) + val))
#             key.append(str(val))
#         return key, "".join(output)


# class Compress:

#     @classmethod
#     async def rle(cls, data):  # Compresses text using RLE
#         output = ''
#         prev_char = ''
#         count = 0
#         for i, char in enumerate(data):
#             if char != prev_char and prev_char != '':
#                 output = output + (f"{count}{prev_char}")
#                 count = 1
#             else:
#                 count += 1
#             prev_char = char
#             await asyncio.sleep(0)
#         return output

#     @classmethod
#     def dict(cls, data, *dictionary):
#         mapping = _gen_map(dictionary)
#         for word, char in mapping.items():
#             data = data.replace(word, char)
#         return (j for i in (hex(ord(char))[2:] for char in cls._rle_space(data)) for j in i)

#     @classmethod
#     def _rle_space(cls, data) -> iter:
#         index = 0
#         length = len(data)
#         while index < length:
#             char = data[index]
#             if char == " " and char == (nc:= data[index+1]):
#                 count = 0
#                 while count < 16 and data[index+2+count] == char:
#                     count += 1
#                 index += count+1
#                 yield from "\u0080\u0080"+hex(count)[2:]
#             else:
#                 yield char
#             index += 1

#     @classmethod
#     def py(cls, data):
#         dictionary = [
#             "self", "def", "class", "core", "format", "return", "if", "else", "elif", "while", "for", "yield", "import", "from", "break", "True", "False", "None",
#             "replace", "@classmethod", "window", "handle", "press", "__init__"
#         ]
#         return cls.dict(data, *dictionary)


# class Convert:

#     @classmethod
#     def ord(cls, string):  # Converts character data into ascii values
#         return [ord(char) for char in string]
