import random
import asyncio


def _gen_map(dictionary):
    return {word: chr(value) for value, word in enumerate(dictionary, start=129)}


class Encrypt:

    @classmethod
    def otk(cls, string):  # Encrypts data using a one-time-key
        key = []
        output = []
        for char in string:
            val = random.randint(0, 30)
            output.append(chr(ord(char) + val))
            key.append(str(val))
        return key, "".join(output)


class Compress:

    @classmethod
    async def rle(cls, data):  # Compresses text using RLE
        output = ''
        prev_char = ''
        count = 0
        for i, char in enumerate(data):
            if char != prev_char and prev_char != '':
                output = output + (f"{count}{prev_char}")
                count = 1
            else:
                count += 1
            prev_char = char
            await asyncio.sleep(0)
        return output

    @classmethod
    def dict(cls, data, *dictionary):
        mapping = _gen_map(dictionary)
        for word, char in mapping.items():
            data = data.replace(word, char)
        return (j for i in (hex(ord(char))[2:] for char in cls._rle_space(data)) for j in i)

    @classmethod
    def _rle_space(cls, data) -> iter:
        index = 0
        length = len(data)
        while index < length:
            char = data[index]
            if char == " " and char == (nc:= data[index+1]):
                count = 0
                while count < 16 and data[index+2+count] == char:
                    count += 1
                index += count+1
                yield from "\u0080\u0080"+hex(count)[2:]
            else:
                yield char
            index += 1

    @classmethod
    def py(cls, data):
        dictionary = [
            "self", "def", "class", "core", "format", "return", "if", "else", "elif", "while", "for", "yield", "import", "from", "break", "True", "False", "None",
            "replace", "@classmethod", "window", "handle", "press", "__init__"
        ]
        return cls.dict(data, *dictionary)


class Convert:

    @classmethod
    def ord(cls, string):  # Converts character data into ascii values
        return [ord(char) for char in string]
