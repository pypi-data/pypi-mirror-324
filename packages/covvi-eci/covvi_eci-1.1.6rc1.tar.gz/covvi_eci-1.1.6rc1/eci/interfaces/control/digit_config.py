
from eci.interfaces.utils import public
from eci.interfaces.enums import Digit
from eci.interfaces.messages import DigitConfigMsg, PinchConfigMsg
from eci.interfaces.control.base_control_interface import BaseControlInterface


class DigitConfigInterface(BaseControlInterface):
    '''An interface to control digit configuration of the hand.'''

    @public
    def getDigitConfig(self, digit: Digit) -> DigitConfigMsg:
        '''Get digit limits'''
        return self._send_recv_RTR(DigitConfigMsg.msg_id + digit)

    @public
    def getPinchConfig(self) -> PinchConfigMsg:
        '''Get pinch points'''
        return self._send_recv_RTR(PinchConfigMsg.msg_id)
