
from eci.interfaces.utils import public
from eci.interfaces.enums import Digit, Digit5, CommandCode
from eci.interfaces.primitives import Command, Percentage, Speed
from eci.interfaces.messages import (
    DigitStatusMsg, DigitStatusAllMsg, DigitPosnMsg, DigitPosnAllMsg, DigitPosnSetMsg,
    DigitMoveMsg, MotorCurrentMsg, MotorCurrentAllMsg, DigitErrorMsg,
)
from eci.interfaces.control.base_control_interface import BaseControlInterface


class DigitInterface(BaseControlInterface):
    '''An interface to control each digit of the hand.'''

    @public
    def getDigitStatus(self, digit: Digit) -> DigitStatusMsg:
        '''Get the digit status flags'''
        return self._send_recv_RTR(DigitStatusMsg.msg_id + digit)

    @public
    def getDigitStatus_all(self) -> DigitStatusAllMsg:
        '''Get all digit status flags'''
        return self._send_recv_RTR(DigitStatusAllMsg.msg_id)

    @public
    def getDigitPosn(self, digit: Digit) -> DigitPosnMsg:
        '''Get the digit position'''
        return self._send_recv_RTR(DigitPosnMsg.msg_id + digit)

    @public
    def getDigitPosn_all(self) -> DigitPosnAllMsg:
        '''Get all digit positions'''
        return self._send_recv_RTR(DigitPosnAllMsg.msg_id)

    @public
    def setDigitPosn(self,   speed: Speed,
            thumb: int = -1, index: int = -1, middle: int = -1, ring: int = -1, little: int = -1, rotate: int = -1) -> DigitPosnSetMsg:
        '''Set the digit position to move to and the movement speed for each digit and thumb rotation'''
        speed, thumb, index, middle, ring, little, rotate = \
            Speed(speed), int(thumb), int(index), int(middle), int(ring), int(little), int(rotate)
        return self._send(DigitPosnSetMsg(cmd_type=Command(CommandCode.CMD), speed=speed,
            thumb  = thumb  >= 0, thumb_pos  = thumb  * (thumb  > 0),  ring   = ring   >= 0, ring_pos   = ring   * (ring   > 0),
            index  = index  >= 0, index_pos  = index  * (index  > 0),  little = little >= 0, little_pos = little * (little > 0),
            middle = middle >= 0, middle_pos = middle * (middle > 0),  rotate = rotate >= 0, rotate_pos = rotate * (rotate > 0),
        ))

    @public
    def setDigitPosnStop(self) -> DigitPosnSetMsg:
        '''Set the digit movement to stop'''
        return self.setDigitPosn(speed=0)

    @public
    def setDigitMove(self, digit: Digit, position: int, speed: Speed, power: Percentage, limit: Percentage) -> DigitMoveMsg:
        '''Command to move a single digit'''
        return self._send(DigitMoveMsg(cmd_type=Command(CommandCode.CMD), msg_id=DigitMoveMsg.msg_id + digit, position=position, speed=speed, power=power, limit=limit))

    @public
    def getMotorCurrent(self, digit: Digit5) -> MotorCurrentMsg:
        '''Get motor current

        Motor current is not available for rotation motor,
        The current value is in multiples of 16mA. e.g. 1 = 16mA, 64 = 1024mA
        '''
        return self._send_recv_RTR(MotorCurrentMsg.msg_id + digit)

    @public
    def getMotorCurrent_all(self) -> MotorCurrentAllMsg:
        '''Get all motor currents

        Motor current is not available for rotation motor,
        The current value is in multiples of 16mA. e.g. 1 = 16mA, 64 = 1024mA
        '''
        return self._send_recv_RTR(MotorCurrentAllMsg.msg_id)

    @public
    def getDigitError(self, digit: Digit) -> DigitErrorMsg:
        '''Get digit error flags'''
        return self._send_recv_RTR(DigitErrorMsg.msg_id + digit)
