
from typing import List
from ctypes import c_short, c_ushort

from eci.messages.enums import (
    NetDevice, MessageID, DigitConfigMessageID, GripNameMessageID,
    ProductID, DeviceClassType, DeviceGlove, DeviceColour, Language,
    GripNameIndex, CommandCode, BulkDataType, UpdateStatus,
)
from eci.messages.primitives import Product, Command, Uint8, Int16
from eci.messages.utils import fStrBits, tobool
from eci.messages.control_message import ControlMsg, RealtimeMsg
from eci.messages.base_message import covvi_message

################################################################################################################################
# Hand power
################################################################################################################################

@covvi_message
class HandPowerMsg(ControlMsg):
    '''A message for turning the power on and off to the hand.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '0000000{enable:01b}'
    dev_id: NetDevice = NetDevice.LOCAL
    msg_id: MessageID = MessageID.nwHandPower
    enable: bool      = True

    def __post_init__(self):
        super().__post_init__()
        self.enable = tobool(self.enable)


@covvi_message
class DeviceInfoMsg(ControlMsg):
    '''A message for retrieving the info of a device on the CANBUS.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{device_id:04b}0{error:01b}{power_on:01b}{connected:01b}{device_class_type:08b}{serial_number:016b}{manufacturer_id:08b}{product_id:08b}'
    msg_id: MessageID = MessageID.nwDeviceInfo
    device_id:         NetDevice       = NetDevice()
    error:             bool            = False
    power_on:          bool            = False
    connected:         bool            = False
    device_class_type: DeviceClassType = DeviceClassType()
    serial_number:     Int16           = Int16(0)
    manufacturer_id:   Uint8           = Uint8(0)
    product_id:        Product         = Product(ProductID())

    def __post_init__(self):
        super().__post_init__()
        self.device_id = NetDevice(self.device_id)
        self.error     =    tobool(self.error)
        self.power_on  =    tobool(self.power_on)
        self.connected =    tobool(self.connected)
        if isinstance(self.device_class_type, str):
            self.device_class_type = int(self.device_class_type)
        if isinstance(self.device_class_type, int):
            self.device_class_type = DeviceClassType(self.device_class_type)
        self.serial_number   = int(self.serial_number)
        self.manufacturer_id = Uint8(int(self.manufacturer_id))
        self.product_id      = Product(int(self.product_id))

    @property
    def dict(self):
        return {**super().dict, **dict(
            device_id         =    int(self.device_id),
            error             = tobool(self.error),
            power_on          = tobool(self.power_on),
            connected         = tobool(self.connected),
            device_class_type =    int(self.device_class_type),
            serial_number     =    int(self.serial_number),
            manufacturer_id   =    int(self.manufacturer_id),
            product_id        =    int(self.product_id),
        )}

################################################################################################################################
# Discovery and device messages
################################################################################################################################

@covvi_message
class HelloMsg(ControlMsg):
    '''A simple message to confirm the link between ECI and software interface.'''
    dev_id: NetDevice = NetDevice.LOCAL
    msg_id: MessageID = MessageID.caHello


@covvi_message
class FirmwareMsg(ControlMsg):
    '''A message for representing the firmware of the ECI.'''
    START_YEAR = 2018
    FORMAT_STR = ControlMsg.FORMAT_STR + '{revision:08b}{major:08b}{minor:08b}'
    dev_id: NetDevice = NetDevice.LOCAL
    msg_id: MessageID = MessageID.caFirmware
    revision: int = 0
    major:    int = 0
    minor:    int = 0

    @property
    def version(self) -> str:
        return f'{self.revision + self.START_YEAR}.{self.major}.{self.minor}'

    def __post_init__(self):
        super().__post_init__()
        self.revision = int(self.revision)
        self.major    = int(self.major)
        self.minor    = int(self.minor)


@covvi_message
class FirmwarePicMsg(FirmwareMsg):
    '''A message for representing the PIC firmware of the ECI.'''
    msg_id: MessageID = MessageID.caFirmware_PIC


@covvi_message
class HandFirmwarePicMsg(FirmwarePicMsg):
    '''A message for representing the PIC firmware of the ECI.'''
    dev_id: NetDevice = NetDevice.HAND


@covvi_message
class EciFirmwarePicMsg(FirmwarePicMsg):
    '''A message for representing the PIC firmware of the ECI.'''
    dev_id: NetDevice = NetDevice.LOCAL


@covvi_message
class FirmwareFpgaMsg(FirmwareMsg):
    '''A message for representing the FPGA firmware of the ECI.'''
    msg_id: MessageID = MessageID.caFirmware_FPGA


@covvi_message
class FirmwareBleMsg(FirmwareMsg):
    '''A message for representing the BLE firmware of the ECI.'''
    msg_id: MessageID = MessageID.caFirmware_BLE


@covvi_message
class FirmwareFramMsg(FirmwareMsg):
    '''A message for representing the FRAM firmware of the ECI.'''
    msg_id: MessageID = MessageID.caFirmware_FRAM


@covvi_message
class FirmwareMaxMsg(FirmwareMsg):
    '''A message for representing the MAX firmware of the ECI.'''
    msg_id: MessageID = MessageID.caFirmware_MAX


@covvi_message
class DeviceIdentityMsg(ControlMsg):
    '''A message for setting the identity parameters of the device.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{type:02b}{wrist:01b}{glove:01b}{colour:04b}{language:04b}{hw_version:04b}{year_of_manufacture:08b}{extended_warranty:04b}{warranty_expires_month:04b}{warranty_expires_year:08b}'
    msg_id: MessageID = MessageID.caDeviceIdentity
    type:                   int          = 0
    wrist:                  bool         = False
    glove:                  DeviceGlove  = DeviceGlove.BLACK
    colour:                 DeviceColour = DeviceColour.WHITE
    language:               Language     = Language.ENGLISH
    hw_version:             int          = 0
    year_of_manufacture:    int          = 0
    extended_warranty:      int          = 0
    warranty_expires_month: int          = 0
    warranty_expires_year:  int          = 0

    def __post_init__(self):
        super().__post_init__()
        self.wrist    = tobool(self.wrist)
        self.glove    = DeviceGlove(int(self.glove))
        self.colour   = DeviceColour(int(self.colour))
        self.language = Language(int(self.language))


@covvi_message
class DeviceProductMsg(ControlMsg):
    '''A message for setting the product parameters of the device.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{manufacturer_id:08b}{product_id:08b}'
    msg_id: MessageID = MessageID.caDeviceProduct
    manufacturer_id: Uint8   = Uint8(0)
    product_id:      Product = Product(ProductID.NONE)

    def __post_init__(self):
        super().__post_init__()
        self.manufacturer_id = Uint8(int(self.manufacturer_id))
        self.product_id      = Product(int(self.product_id))

    @property
    def dict(self):
        return {**super().dict, **dict(manufacturer_id=int(self.manufacturer_id), product_id=int(self.product_id))}

################################################################################################################################
# Digit configuration messages
################################################################################################################################

@covvi_message
class DigitConfigMsg(ControlMsg):
    '''A message for configuring the open/close limits and offset of a hand digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{open_limit:08b}{close_limit:08b}{offset:08b}'
    msg_id: MessageID = MessageID.caDigitConfig
    open_limit:  int = 0
    close_limit: int = 0
    offset:      int = 0

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(DigitConfigMessageID)
        self.open_limit  = int(self.open_limit)
        self.close_limit = int(self.close_limit)
        self.offset      = int(self.offset)


@covvi_message
class PinchConfigMsg(ControlMsg):
    '''A message for configuring the position at which a digit has reached its pinch point.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        fStrBits('thumb index middle one_finger_rotate two_finger_rotate', 'pos', k=8)
    msg_id: MessageID = MessageID.caPinchConfig
    thumb_pos:             int = 0
    index_pos:             int = 0
    middle_pos:            int = 0
    one_finger_rotate_pos: int = 0
    two_finger_rotate_pos: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.thumb_pos             = int(self.thumb_pos)
        self.index_pos             = int(self.index_pos)
        self.middle_pos            = int(self.middle_pos)
        self.one_finger_rotate_pos = int(self.one_finger_rotate_pos)
        self.two_finger_rotate_pos = int(self.two_finger_rotate_pos)

################################################################################################################################
# Grip configuration messages
################################################################################################################################

@covvi_message
class GripNameMsg(ControlMsg):
    '''A message for retrieving one of the grip names. The whole grip name may be split into multiple 'GripNameMsg's.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{msg_num:04b}{msg_total:04b}{ch1:08b}{ch2:08b}{ch3:08b}{ch4:08b}{ch5:08b}{ch6:08b}{ch7:08b}'
    msg_id: MessageID = MessageID.caGripName
    msg_num:   int = 1
    msg_total: int = 1
    ch1:       int = 0
    ch2:       int = 0
    ch3:       int = 0
    ch4:       int = 0
    ch5:       int = 0
    ch6:       int = 0
    ch7:       int = 0

    @property
    def char_args(self) -> List[int]:
        return [self.ch1, self.ch2, self.ch3, self.ch4, self.ch5, self.ch6, self.ch7]

    @property
    def chars(self) -> str:
        return ''.join(chr(ch) for ch in self.char_args if ch > 0)

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(GripNameMessageID)
        self.msg_num   = int(self.msg_num)
        self.msg_total = int(self.msg_total)
        self.ch1       = int(self.ch1)
        self.ch2       = int(self.ch2)
        self.ch3       = int(self.ch3)
        self.ch4       = int(self.ch4)
        self.ch5       = int(self.ch5)
        self.ch6       = int(self.ch6)
        self.ch7       = int(self.ch7)

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + 'ch1 ch2 ch3 ch4 ch5 ch6 ch7'.split(),
            ['', *self.char_args],
        ], width=5)

################################################################################################################################
# System and status messages
################################################################################################################################

@covvi_message
class EnvironmentalMsg(RealtimeMsg):
    '''A message for reading the environmental information of the hand. I.E. temperature, humidity, and battery voltage.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{temperature:08b}{humidity:08b}{battery_voltage:016b}'
    msg_id: MessageID = MessageID.caEnvironmental
    temperature:     int   = 0
    humidity:        int   = 0
    battery_voltage: Int16 = Int16(0)

    def __post_init__(self):
        super().__post_init__()
        self.temperature     =   int(self.temperature)
        self.humidity        =   int(self.humidity)
        self.battery_voltage = Int16(self.battery_voltage)


@covvi_message
class SystemStatusMsg(RealtimeMsg):
    '''A message for reading the system status of the hand. I.E. critical error flags, non-fatal errors, bluetooth status, and change notifications.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '00000{bluetooth_fault:01b}{spi_error:01b}{gateway_error:01b}' + \
        '000000{humidity_limit:01b}{temperature_limit:01b}' + \
        '{bluetooth_status:08b}{change_notifications:08b}'
    msg_id: MessageID = MessageID.caSystemStatus

    bluetooth_fault:      bool = False
    spi_error:            bool = False
    gateway_error:        bool = False

    humidity_limit:       bool = False
    temperature_limit:    bool = False

    bluetooth_status:     int = 0
    change_notifications: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.bluetooth_fault      = tobool(self.bluetooth_fault)
        self.spi_error            = tobool(self.spi_error)
        self.gateway_error        = tobool(self.gateway_error)
        self.humidity_limit       = tobool(self.humidity_limit)
        self.temperature_limit    = tobool(self.temperature_limit)
        self.bluetooth_status     =    int(self.bluetooth_status)
        self.change_notifications =    int(self.change_notifications)


@covvi_message
class OrientationMsg(RealtimeMsg):
    '''A message for reading the orientation of the hand.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{x:016b}{y:016b}{z:016b}'
    msg_id: MessageID = MessageID.caOrientation
    x: Int16 = Int16(0)
    y: Int16 = Int16(0)
    z: Int16 = Int16(0)
    X = Int16(0)
    Y = Int16(0)
    Z = Int16(0)

    def __post_init__(self):
        super().__post_init__()
        self.x = Int16(c_short(self.x).value) - self.X
        self.y = Int16(c_short(self.y).value) - self.Y
        self.z = Int16(c_short(self.z).value) - self.Z

    def pack(self, *args, **kwargs) -> bytes:
        return super().pack(
            *args,
            x=c_ushort(self.x + self.X).value,
            y=c_ushort(self.y + self.Y).value,
            z=c_ushort(self.z + self.Z).value,
            **kwargs,
        )

    @property
    def dict(self):
        return {**super().dict, **dict(
            x=c_ushort(self.x + self.X).value,
            y=c_ushort(self.y + self.Y).value,
            z=c_ushort(self.z + self.Z).value,
        )}


@covvi_message
class MotorLimitsMsg(RealtimeMsg):
    '''A message for reading the motor limiting values of the hand. If the motors are deemed to be too hot, the power is limited.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{hand:01b}{eci:01b}0{ltl:01b}{rng:01b}{mid:01b}{idx:01b}{thb:01b}' + \
        '{thumb_derate_value:08b}{index_derate_value:08b}{middle_derate_value:08b}{ring_derate_value:08b}{little_derate_value:08b}'
    msg_id: MessageID = MessageID.caMotorLimits
    hand:                bool = False
    eci:                 bool = False
    ltl:                 bool = False
    rng:                 bool = False
    mid:                 bool = False
    idx:                 bool = False
    thb:                 bool = False
    thumb_derate_value:  int  = 0
    index_derate_value:  int  = 0
    middle_derate_value: int  = 0
    ring_derate_value:   int  = 0
    little_derate_value: int  = 0

    def __post_init__(self):
        super().__post_init__()
        self.hand                = tobool(self.hand)
        self.eci                 = tobool(self.eci)
        self.ltl                 = tobool(self.ltl)
        self.rng                 = tobool(self.rng)
        self.mid                 = tobool(self.mid)
        self.idx                 = tobool(self.idx)
        self.thb                 = tobool(self.thb)
        self.thumb_derate_value  =    int(self.thumb_derate_value)
        self.index_derate_value  =    int(self.index_derate_value)
        self.middle_derate_value =    int(self.middle_derate_value)
        self.ring_derate_value   =    int(self.ring_derate_value)
        self.little_derate_value =    int(self.little_derate_value)

################################################################################################################################
# Firmware update messages
################################################################################################################################

@covvi_message
class UploadDownLoadMsg(ControlMsg):
    FORMAT_STR = ControlMsg.FORMAT_STR + '{data_type:04b}'
    msg_id:    MessageID    = MessageID.caUpdateDownload
    data_type: BulkDataType = BulkDataType.GRIP

    def __post_init__(self):
        super().__post_init__()
        self.data_type = BulkDataType(int(self.data_type))

################################################################

@covvi_message
class UserGripMsg(UploadDownLoadMsg):
    FORMAT_STR = UploadDownLoadMsg.FORMAT_STR + '{grip_name_index:04b}'
    grip_name_index: GripNameIndex = GripNameIndex.GN0

    def __post_init__(self):
        super().__post_init__()
        self.grip_name_index = GripNameIndex(int(self.grip_name_index))


@covvi_message
class UserGripResMsg(UserGripMsg):
    '''A message to represent a user grip response.'''
    FORMAT_STR = UserGripMsg.FORMAT_STR + '{update_status:08b}' + '0'*8
    cmd_type: Command = Command(CommandCode.RES)
    update_status: UpdateStatus = UpdateStatus.Ok

    def __post_init__(self):
        super().__post_init__()
        self.update_status = UpdateStatus(int(self.update_status))

################################################################

@covvi_message
class UserGripCmdMsg(UserGripMsg):
    cmd_type: Command = Command(CommandCode.CMD)


@covvi_message
class SendUserGripCmdMsg(UserGripCmdMsg):
    '''A message for initiating the sending of a user grip to the hand.'''
    FORMAT_STR = UserGripCmdMsg.FORMAT_STR + '{file_len:024b}{major_version:08b}{minor_version:08b}' + '0'*8
    file_len:      int = 0
    major_version: int = 0
    minor_version: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.file_len      = int(self.file_len)
        self.major_version = int(self.major_version)
        self.minor_version = int(self.minor_version)


@covvi_message
class RemoveUserGripCmdMsg(UserGripCmdMsg):
    '''A message for initiating the removal of a user grip.'''
    FORMAT_STR = UserGripCmdMsg.FORMAT_STR + '0'*8*2 + f'{16:08b}' + '0'*8*3

################################################################################################################################
