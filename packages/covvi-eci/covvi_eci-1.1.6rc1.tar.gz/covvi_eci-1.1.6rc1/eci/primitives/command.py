
from typing      import overload
from dataclasses import dataclass

from eci.primitives.enums          import CommandString, CommandCode
from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class Command(BasePrimitive):
    value: CommandString = CommandString.CMD
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, integer: int): ...
    @overload
    def __init__(self, command_code: CommandCode): ...
    @overload
    def __init__(self, command_string: CommandString): ...
    def __init__(self, value = CommandString.CMD):
        if isinstance(value, str):
            self.value = CommandString(value)
            return
        if isinstance(value, int):
            self.value = CommandCode(value).str()
            return
        if isinstance(value, CommandCode):
            self.value = value.str()
            return
        if isinstance(value, CommandString):
            self.value = value
            return
        if isinstance(value, Command):
            self.value = value.value
            return

    def __str__(self) -> str:
        return str(self.value)
    def __int__(self) -> int:
        return int(self.value.int()) & 0xF
    def str(self) -> CommandString:
        return self.value
    def int(self) -> CommandCode:
        return self.value.int()


Command.__doc__ = f'''This is a class to represent a command type in a ControlMsg. Its possible values are:
{', '.join([command_code.name for command_code in CommandCode])}.'''
