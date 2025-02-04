
from dataclasses import dataclass
from warnings    import warn

from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class Percentage(BasePrimitive):
    '''This is a class to represent a percentage value. I.E. a speed, power, or limit value.'''
    MAX = 100
    MIN = 0
    value: int = 0

    def __init__(self, value: int = MIN):
        if issubclass(type(value), Percentage):
            value = value.value

        if value < self.MIN:
            warn(f'The value provided ({value}) was lower than the minimum value ({self.MIN}) for {type(self)}.')
            value = self.MIN
        elif value > self.MAX:
            warn(f'The value provided ({value}) was higher than the maximum value ({self.MAX}) for {type(self)}.')
            value = self.MAX

        self.value = int(value)

    def __str__(self) -> str:
        return str(self.value)
    def __int__(self) -> int:
        return int(self.value)
