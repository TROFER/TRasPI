class Singleton(type):

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]
        new_cls = super().__call__(*args, **kwargs)
        cls._instances[cls] = new_cls
        return new_cls
