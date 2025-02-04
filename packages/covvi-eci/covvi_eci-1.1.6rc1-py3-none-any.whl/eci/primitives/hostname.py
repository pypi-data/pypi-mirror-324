
from typing      import overload
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class Hostname(BasePrimitive):
    '''This is a class to represent a hostname in a discovery message.'''
    value: str = ''
    @overload
    def __init__(self, integer: int): ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, b: bytes): ...
    def __init__(self, *args):
        if len(args) == 0:
            self.value = ''
            return
        if len(args) == 1:
            arg, *_ = args
            if type(arg) is int:
                self.value = arg.to_bytes(256 // 8, byteorder='big').replace(b'\xFE', b'').replace(b'\x00', b'').decode()
                return
            if type(arg) is str:
                self.value = arg
                return
            if type(arg) is Hostname:
                self.value = arg.value
                return
            if type(arg) is bytes:
                self.value = arg.replace(b'\xFE', b'').replace(b'\x00', b'').decode()
                return
        raise ValueError('__init__ takes a single string or a bytes object')

    def __bytes__(self) -> bytes:
        return (self.value + '\x00' * ((256 // 8) - len(self.value))).encode()
    def __int__(self) -> int:
        return int.from_bytes(bytes(self), byteorder='big')
    def __str__(self) -> str:
        return self.value
