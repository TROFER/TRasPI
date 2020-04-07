import random


class Encrypt:

    @classmethod
    def encrypt_otk(cls, string):  # Encrypts data using a one-time-key
    key = []
    output = []
    for char in string:
        val = random.randint(0, 30)
        output.append(chr(ord(char) + val))
        key.append(str(val))
    return key, "".join(output)


class Compress:

    @classmethod
    def compress_rle(cls, data):  # Compresses text using RLE
        output = ''
        prev_char = ''
        count = 0
        for char in data:
            if char != prev_char and prev_char != '':
                output = output + (f"{count}{prev_char}")
                count = 1
            else:
                count += 1
            prev_char = char
        return output


class Convert:

    @classmethod
    def convert_ord(cls, string):  # Converts character data into ascii values
        return [ord(char) for char in string]
