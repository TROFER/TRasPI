__all__ = ["Singleton"]

class Singleton(type):

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]
        self = super().__call__(*args, **kwargs)
        cls._instances[cls] = self
        return self
