
from re          import Pattern, Match, compile, search
from typing      import Tuple, overload
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


N_OCTETS:                  int     = 6
MAC_OCTET_REGEX:           str     = '([0-9a-zA-Z]{1,2})'
MAC_REGEX:                 Pattern = compile('[:]'.join([MAC_OCTET_REGEX] * N_OCTETS))
SIX_OCTET_ADDRESS_DEFAULT: str     = ':'.join(['00'] * N_OCTETS)


@dataclass(unsafe_hash=True)
class SixOctetAddress(BasePrimitive):
    '''This is a class to represent a network address of six octets. I.E. MAC addresses.'''
    value: str = SIX_OCTET_ADDRESS_DEFAULT
    @overload
    def __init__(self, integer: int): ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, a: int, b: int, c: int, d: int, e: int, f: int): ...
    def __init__(self, *args):
        if len(args) == 0:
            self.value = SIX_OCTET_ADDRESS_DEFAULT
            return
        if len(args) == 1:
            arg, *_ = args
            if type(arg) is int:
                self.value = SixOctetAddress.int_to_str(arg)
                return
            if type(arg) is SixOctetAddress:
                self.value = arg.value
                return
            if type(arg) is str:
                self.value = arg
                return
        if len(args) == N_OCTETS:
            self.value = SixOctetAddress.ints_to_str(*args)
            return
        raise ValueError(f'__init__ takes a single string or int or {N_OCTETS} integers')

    def __int__(self) -> int:
        return SixOctetAddress.str_to_int(self.value)
    def __str__(self) -> str:
        return self.value

    @classmethod
    def int_to_str(self, arg: int) -> str:
        return ':'.join([f'{(arg >> i) & 0xFF:02X}' for i in range(0, 8 * N_OCTETS, 8)[::-1]])

    @classmethod
    def ints_to_str(self, *args: Tuple[int]) -> str:
        return SixOctetAddress.int_to_str(sum([(int(b) & 0xFF) << (i * 8) for i, b in enumerate(args[::-1])]))

    @classmethod
    def str_to_int(self, arg: str) -> int:
        matched: Match = search(MAC_REGEX, arg).groups()[::-1]
        return sum([(int(b, base=0x10) & 0xFF) << (i * 8) for i, b in enumerate(matched)])
