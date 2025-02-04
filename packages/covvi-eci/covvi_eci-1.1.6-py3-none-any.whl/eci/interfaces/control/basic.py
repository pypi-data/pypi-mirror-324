
from eci.interfaces.utils import public
from eci.interfaces.primitives import Command, CommandCode
from eci.interfaces.messages import (
    HelloMsg, DeviceIdentityMsg, DeviceProductMsg,
    EciFirmwarePicMsg, HandFirmwarePicMsg,
    FirmwareFpgaMsg, FirmwareBleMsg, FirmwareFramMsg, FirmwareMaxMsg,
)
from eci.interfaces.control.base_control_interface import BaseControlInterface


class BasicControlInterface(BaseControlInterface):
    '''An interface to control discovery and device messages.'''

    @public
    def getHello(self) -> HelloMsg:
        return self._send_recv_RTR(HelloMsg.msg_id)

    @public
    def getFirmware_PIC_HAND(self) -> HandFirmwarePicMsg:
        self._send(HandFirmwarePicMsg(cmd_type=Command(CommandCode.RTR)))
        return self._get_message(HandFirmwarePicMsg)

    @public
    def getFirmware_PIC_ECI(self) -> EciFirmwarePicMsg:
        self._send(EciFirmwarePicMsg(cmd_type=Command(CommandCode.RTR)))
        return self._get_message(EciFirmwarePicMsg)

    @public
    def getDeviceIdentity(self) -> DeviceIdentityMsg:
        return self._send_recv_RTR(DeviceIdentityMsg.msg_id)

    @public
    def getDeviceProduct(self) -> DeviceProductMsg:
        return self._send_recv_RTR(DeviceProductMsg.msg_id)
