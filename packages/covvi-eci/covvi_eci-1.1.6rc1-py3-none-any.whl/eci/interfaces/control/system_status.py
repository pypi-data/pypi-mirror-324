
from eci.interfaces.utils import public
from eci.interfaces.messages import EnvironmentalMsg, SystemStatusMsg, OrientationMsg, MotorLimitsMsg
from eci.interfaces.control.base_control_interface import BaseControlInterface


class SystemStatusInterface(BaseControlInterface):
    '''An interface to control System and status messages of the hand.'''

    @public
    def getEnvironmental(self) -> EnvironmentalMsg:
        '''Read temperature, battery voltage etc

        Temperature     (C)
        Humidity        (0-100%)
        Battery Voltage (mV)
        '''
        return self._send_recv_RTR(EnvironmentalMsg.msg_id)

    @public
    def getSystemStatus(self) -> SystemStatusMsg:
        '''Read system status

        Critical error flags
        Non-fatal errors
        Bluetooth Status
        Change Notifications
        '''
        return self._send_recv_RTR(SystemStatusMsg.msg_id)

    @public
    def getOrientation(self) -> OrientationMsg:
        '''Get hand orientation

        X Position
        Y Position
        Z Position
        '''
        return self._send_recv_RTR(OrientationMsg.msg_id)

    @public
    def getMotorLimits(self) -> MotorLimitsMsg:
        '''Get motor limits'''
        return self._send_recv_RTR(MotorLimitsMsg.msg_id)
