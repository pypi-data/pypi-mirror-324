
from eci.interfaces.utils import public
from eci.interfaces.primitives import Command, Speed
from eci.interfaces.enums import DirectControlCommand, CommandCode
from eci.interfaces.messages import DirectControlMsg
from eci.interfaces.control.base_control_interface import BaseControlInterface


class DirectControlInterface(BaseControlInterface):
    '''An interface for direct control of the hand.'''

    def _setDirectControl(self, command: DirectControlCommand, speed: Speed) -> DirectControlMsg:
        return self._send(DirectControlMsg(cmd_type=Command(CommandCode.CMD), command=command, speed=Speed(value=speed)))

    @public
    def setDirectControlOpen(self, speed: Speed = Speed(value=50)) -> DirectControlMsg:
        return self._setDirectControl(command=DirectControlCommand.OPEN, speed=speed)

    @public
    def setDirectControlClose(self, speed: Speed = Speed(value=50)) -> DirectControlMsg:
        return self._setDirectControl(command=DirectControlCommand.CLOSE, speed=speed)

    @public
    def setDirectControlStop(self) -> DirectControlMsg:
        return self._setDirectControl(command=DirectControlCommand.STOP, speed=0)
