import PIL.ImageFont

class _Font(type):

    _instances = set()

    def __call__(cls, name: str, path: (str, int), size: int=None):
        if size is None:
            if isinstance(path, int):
                size = path
                for data in cls._instances:
                    if name in data:
                        name, path = data
                        break
            else:
                cls._instances.add((name, path))
                return None
        else:
            cls._instances.add((name, path))
        return super().__call__(name, path, size)

class Font(metaclass=_Font):

    def __init__(self, name: str, path: (str, int), size: int=None):
        self._name = name
        self._path = path
        self._size = size
        self._compute_font()

    @property
    def name(self) -> str:
        return self._name
    @property
    def path(self) -> str:
        return self._path

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = value
        self._compute_font()

    @property
    def font(self):
        return self._font

    def font_size(self, text) -> int:
        return self._font.getsize(text)

    def _compute_font(self):
        self._font = PIL.ImageFont.truetype(self._path, self._size)
        return self._font
