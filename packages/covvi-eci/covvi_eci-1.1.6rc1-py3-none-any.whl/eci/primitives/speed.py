
from dataclasses import dataclass
from warnings    import catch_warnings, simplefilter

from eci.primitives.percentage import Percentage


@dataclass(unsafe_hash=True)
class Speed(Percentage):
    '''This is a class to represent a speed value.'''
    MAX = 100
    MIN = 15

    def __init__(self, value: int = MIN):
        value = int(value)
        if value == 0:
            with catch_warnings():
                simplefilter('ignore')
                super().__init__(value)
        else:
            super().__init__(value)
