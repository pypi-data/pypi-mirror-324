
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class RealtimeCfg(BasePrimitive):
    digit_status:    bool = False
    digit_posn:      bool = False
    current_grip:    bool = False
    electrode_value: bool = False
    input_status:    bool = False
    motor_current:   bool = False
    digit_touch:     bool = False
    digit_error:     bool = False
    environmental:   bool = False
    orientation:     bool = False
    motor_limits:    bool = False


RealtimeCfg.__doc__ = f'''This is a class to represent a the Realtime Configuration.'''
