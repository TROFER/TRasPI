__all__ = ["Constant"]

class MetaConstant(type):

    def __delattr__(self, attr):
        raise AttributeError("Can not modify Constants")

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("Can not modify Constants")
        super().__setattr__(name, value)

class Constant(metaclass=MetaConstant):
    pass