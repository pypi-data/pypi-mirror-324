
from typing      import overload
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class GripName(BasePrimitive):
    '''This is a class to represent a Grip Name from a GripNameMsg message.'''
    value: str = ''
    @overload
    def __init__(self, string: str): ...
    def __init__(self, *args):
        if len(args) == 0:
            self.value = ''
            return
        if len(args) == 1:
            arg, *_ = args
            if type(arg) is str:
                self.value = arg
                return
            if type(arg) is GripName:
                self.value = arg.value
                return
        raise ValueError('__init__ takes a single string')

    def __eq__(self, value) -> bool:
        if isinstance(value, str):
            return self.value == value
        if isinstance(value, GripName):
            return self.value == value.value
        return False

    def __ne__(self, value) -> bool:
        return not self.__eq__(value)

    def __str__(self) -> str:
        return self.value
