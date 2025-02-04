
from datetime import datetime
from time     import sleep
from logging  import debug
from typing   import Union

from eci.utils                 import to_base, BASE_STRING
from eci.interfaces.utils      import public
from eci.interfaces.control    import ControlInterface
from eci.interfaces.realtime   import RealtimeInterface
from eci.interfaces.messages   import HandPowerMsg, DeviceInfoMsg, OrientationMsg
from eci.interfaces.primitives import FourOctetAddress, Uint8, Int16, Product
from eci.interfaces.enums      import CommandCode, NetDevice, DeviceClassType


class CovviInterface(RealtimeInterface, ControlInterface):
    '''An interface to combine all functionality from all the interfaces into a single one, except 'DiscoveryInterface'.'''

    HAND_POWERED_ON_TIMEOUT = 2**-4
    ENTER_EXIT_DELAY        = 2**-2

    def __init__(self, host: Union[FourOctetAddress, str]):
        debug('Initializing the Covvi Interface')
        super(ControlInterface, self).__init__(host)
        RealtimeInterface.__init__(self, None, None)
        self._eci_device_info_msg:  DeviceInfoMsg = DeviceInfoMsg()
        self._hand_device_info_msg: DeviceInfoMsg = DeviceInfoMsg()
        self._hand_powered_on:      bool          = False
        self._message_dict[DeviceInfoMsg] = self._process_DeviceInfoMsg
        debug('Initialized the Covvi Interface')

    def __enter__(self):
        debug('Starting the Covvi Interface')
        sleep(CovviInterface.ENTER_EXIT_DELAY)
        super(ControlInterface, self).__enter__()
        self.local_host, self.local_port = self._ctl_socket.getsockname()
        RealtimeInterface.__enter__(self)
        debug('Started the Covvi Interface')
        return self

    def __exit__(self, *args):
        debug('Closing the Covvi Interface')
        RealtimeInterface.__exit__(self)
        super(ControlInterface, self).__exit__()
        sleep(CovviInterface.ENTER_EXIT_DELAY)
        debug('Closed the Covvi Interface')

    def __str__(self) -> str:
        return f'''
COVVI Interface ({to_base(id(self), len(BASE_STRING))}) {datetime.now()}
----------------------------------------------------------------
ECI Error:              {self.eci_error}
ECI Power On:           {self.eci_power_on}
ECI Connected:          {self.eci_connected}
ECI Device Class Type:  {self.eci_device_class_type}
ECI Serial Number:      {self.eci_serial_number}
ECI Manufacturer ID:    {self.eci_manufacturer_id}
ECI Product ID:         {self.eci_product_id}
Hand Error:             {self.hand_error}
Hand Power On:          {self.hand_power_on}
Hand Connected:         {self.hand_connected}
Hand Device Class Type: {self.hand_device_class_type}
Hand Serial Number:     {self.hand_serial_number}
Hand Manufacturer ID:   {self.hand_manufacturer_id}
Hand Product ID:        {self.hand_product_id}
'''

    ################################################################

    def _process_DeviceInfoMsg(self, msg: DeviceInfoMsg) -> None:

        if msg.device_id == NetDevice.D0:
            self._eci_device_info_msg = msg

        if msg.device_id == NetDevice.D1:
            self._hand_device_info_msg = msg
            self._hand_powered_on = msg.connected

    def _setHandPower(self, enable: bool) -> HandPowerMsg:
        return self._send(HandPowerMsg(cmd_type=CommandCode.CMD, enable=enable))

    ################################################################

    @property
    def hand_powered_on(self) -> bool:
        return self._hand_powered_on

    @property
    def eci_error(self) -> bool:
        return self._eci_device_info_msg.error
    @property
    def eci_power_on(self) -> bool:
        return self._eci_device_info_msg.power_on
    @property
    def eci_connected(self) -> bool:
        return self._eci_device_info_msg.connected
    @property
    def eci_device_class_type(self) -> DeviceClassType:
        return self._eci_device_info_msg.device_class_type
    @property
    def eci_serial_number(self) -> Int16:
        return self._eci_device_info_msg.serial_number
    @property
    def eci_manufacturer_id(self) -> Uint8:
        return self._eci_device_info_msg.manufacturer_id
    @property
    def eci_product_id(self) -> Product:
        return self._eci_device_info_msg.product_id

    @property
    def hand_error(self) -> bool:
        return self._hand_device_info_msg.error
    @property
    def hand_power_on(self) -> bool:
        return self._hand_device_info_msg.power_on
    @property
    def hand_connected(self) -> bool:
        return self._hand_device_info_msg.connected
    @property
    def hand_device_class_type(self) -> DeviceClassType:
        return self._hand_device_info_msg.device_class_type
    @property
    def hand_serial_number(self) -> Int16:
        return self._hand_device_info_msg.serial_number
    @property
    def hand_manufacturer_id(self) -> Uint8:
        return self._hand_device_info_msg.manufacturer_id
    @property
    def hand_product_id(self) -> Product:
        return self._hand_device_info_msg.product_id

    ################################################################

    @public
    def setHandPowerOn(self) -> HandPowerMsg:
        '''Power on the hand'''
        debug('Powering on the hand')
        r = self._setHandPower(True)
        debug('Waiting for the hand to power on')
        while not self.hand_powered_on:
            sleep(CovviInterface.HAND_POWERED_ON_TIMEOUT)
        self.setRealtimeCfg(orientation = True)
        return r

    @public
    def setHandPowerOff(self) -> HandPowerMsg:
        '''Power off the hand'''
        debug('Powering off the hand')
        r = self._setHandPower(False)
        self._hand_powered_on = False
        return r

    ################################################################

    @public
    def resetRealtimeCfg(self):
        self.setRealtimeCfg()
        RealtimeInterface.resetRealtimeCfg(self)

    @public
    def getOrientation(self) -> OrientationMsg:
        '''Get hand orientation

        X Position
        Y Position
        Z Position
        '''
        if type(self.orientation_msg) == type(None):
            self.orientation_msg = ControlInterface.getOrientation(self)
        return self.orientation_msg

    ################################################################

    @public
    def getEciError(self) -> bool:
        '''Get the error status of the ECI'''
        return self.eci_error
    @public
    def getEciPowerOn(self) -> bool:
        '''Get the 'power on' status of the ECI'''
        return self.eci_power_on
    @public
    def getEciConnected(self) -> bool:
        '''Get the connected status of the ECI'''
        return self.eci_connected
    @public
    def getEciDeviceClassType(self) -> DeviceClassType:
        '''Get the 'device class' of the ECI'''
        return self.eci_device_class_type
    @public
    def getEciSerialNumber(self) -> Int16:
        '''Get the serial number of the ECI'''
        return self.eci_serial_number
    @public
    def getEciManufacturerID(self) -> Uint8:
        '''Get the manufacturer ID of the ECI'''
        return self.eci_manufacturer_id
    @public
    def getEciProductID(self) -> Product:
        '''Get the product ID of the ECI'''
        return self.eci_product_id

    @public
    def getHandError(self) -> bool:
        '''Get the error status of the Hand'''
        return self.hand_error
    @public
    def getHandPowerOn(self) -> bool:
        '''Get the 'power on' status of the Hand'''
        return self.hand_power_on
    @public
    def getHandConnected(self) -> bool:
        '''Get the connected status of the Hand'''
        return self.hand_connected
    @public
    def getHandDeviceClassType(self) -> DeviceClassType:
        '''Get the 'device class' of the Hand'''
        return self.hand_device_class_type
    @public
    def getHandSerialNumber(self) -> Int16:
        '''Get the serial number of the Hand'''
        return self.hand_serial_number
    @public
    def getHandManufacturerID(self) -> Uint8:
        '''Get the manufacturer ID of the Hand'''
        return self.hand_manufacturer_id
    @public
    def getHandProductID(self) -> Product:
        '''Get the product ID of the Hand'''
        return self.hand_product_id
