
from re          import Pattern, Match, compile, search
from typing      import Tuple, overload
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


N_OCTETS:                   int     = 4
IP_OCTET_REGEX:             str     = '([0-9]{1,3})'
IP_REGEX:                   Pattern = compile('[.]'.join([IP_OCTET_REGEX] * N_OCTETS))
FOUR_OCTET_ADDRESS_DEFAULT: str     = '.'.join('0' * N_OCTETS)


@dataclass(unsafe_hash=True)
class FourOctetAddress(BasePrimitive):
    '''This is a class to represent a network address of four octets. I.E. IPv4 addresses and Subnet masks.'''
    value: str = FOUR_OCTET_ADDRESS_DEFAULT
    @overload
    def __init__(self, integer: int): ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, a: int, b: int, c: int, d: int): ...
    def __init__(self, *args):
        if len(args) == 0:
            self.value = FOUR_OCTET_ADDRESS_DEFAULT
            return
        if len(args) == 1:
            arg, *_ = args
            if type(arg) is int:
                self.value = FourOctetAddress.int_to_str(arg)
                return
            if type(arg) is FourOctetAddress:
                self.value = arg.value
                return
            if type(arg) is str:
                if arg == '':
                    arg = FOUR_OCTET_ADDRESS_DEFAULT
                self.value = arg
                return
        if len(args) == N_OCTETS:
            self.value = FourOctetAddress.ints_to_str(*args)
            return
        raise ValueError(f'__init__ takes a single string or int or {N_OCTETS} integers')

    def __int__(self) -> int:
        return FourOctetAddress.str_to_int(self.value)
    def __str__(self) -> str:
        return self.value

    @classmethod
    def int_to_str(self, arg: int) -> str:
        return '.'.join([f'{(arg >> i) & 0xFF}' for i in range(0, 8 * N_OCTETS, 8)[::-1]])

    @classmethod
    def ints_to_str(self, *args: Tuple[int]) -> str:
        return FourOctetAddress.int_to_str(sum([(int(b) & 0xFF) << (i * 8) for i, b in enumerate(args[::-1])]))

    @classmethod
    def str_to_int(self, arg: str) -> int:
        matched: Match = search(IP_REGEX, arg).groups()[::-1]
        return sum([(int(b) & 0xFF) << (i * 8) for i, b in enumerate(matched)])
