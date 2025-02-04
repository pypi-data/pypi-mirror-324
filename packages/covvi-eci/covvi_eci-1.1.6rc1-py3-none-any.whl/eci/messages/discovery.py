
from typing import Dict, Any
from eci.messages.utils import tobool
from eci.messages.enums import DeviceClassType, ProductID
from eci.messages.primitives import FourOctetAddress, SixOctetAddress, Hostname, Product, Uint8, Int16
from eci.messages.base_message import BaseMessage, covvi_message


fStrDiscoResponseBody = '''
{discovery_version:016b}{device_serial_number:016b}{mac:048b}{device_class_type:08b}
00000000
{manufacturer_id:08b}{product_id:08b}
{ip:032b}{subnet_mask:032b}{gateway:032b}{dns:032b}{hostname:0256b}
0000000
{dhcp:01b}
00000
{hand_comms:01b}{hand_power:01b}{client_connected:01b}
0000000000000000
{client_address:032b}{request_source_address:032b}
'''


class DiscoveryMsg(BaseMessage):
    ...


@covvi_message
class DiscoveryRequestMsg(DiscoveryMsg):
    '''The message for requesting discovery information from the ECI. This message is broadcasted.'''
    FORMAT_STR = f'{0x0401:016b}'


@covvi_message
class DiscoveryBaseMsg(DiscoveryMsg):
    discovery_version:      Int16            = Int16(2)
    device_serial_number:   Int16            = Int16(0)
    mac:                    SixOctetAddress  = SixOctetAddress()
    device_class_type:      DeviceClassType  = DeviceClassType()
    manufacturer_id:        int              = Uint8(0)
    product_id:             Product          = Product(ProductID())
    ip:                     FourOctetAddress = FourOctetAddress()
    subnet_mask:            FourOctetAddress = FourOctetAddress()
    gateway:                FourOctetAddress = FourOctetAddress()
    dns:                    FourOctetAddress = FourOctetAddress()
    hostname:               Hostname         = Hostname()
    dhcp:                   bool             = False
    hand_comms:             bool             = False
    hand_power:             bool             = False
    client_connected:       bool             = False
    client_address:         FourOctetAddress = FourOctetAddress()
    request_source_address: FourOctetAddress = FourOctetAddress()

    def __post_init__(self):
        super().__post_init__()
        self.discovery_version      =            Int16(self.discovery_version)
        self.device_serial_number   =            Int16(self.device_serial_number)
        self.mac                    =  SixOctetAddress(self.mac)
        self.device_class_type      =  DeviceClassType(self.device_class_type)
        self.manufacturer_id        =            Uint8(self.manufacturer_id)
        self.product_id             =          Product(self.product_id)
        self.ip                     = FourOctetAddress(self.ip)
        self.subnet_mask            = FourOctetAddress(self.subnet_mask)
        self.gateway                = FourOctetAddress(self.gateway)
        self.dns                    = FourOctetAddress(self.dns)
        self.hostname               =         Hostname(self.hostname)
        self.dhcp                   =           tobool(self.dhcp)
        self.hand_comms             =           tobool(self.hand_comms)
        self.hand_power             =           tobool(self.hand_power)
        self.client_connected       =           tobool(self.client_connected)
        self.client_address         = FourOctetAddress(self.client_address)
        self.request_source_address = FourOctetAddress(self.request_source_address)

    @property
    def dict(self) -> Dict[str, Any]:
        return {**super().dict, **dict(
            discovery_version      =    int(self.discovery_version),
            device_serial_number   =    int(self.device_serial_number),
            mac                    =    str(self.mac),
            device_class_type      =    int(self.device_class_type),
            manufacturer_id        =    int(self.manufacturer_id),
            product_id             =    int(self.product_id),
            ip                     =    str(self.ip),
            subnet_mask            =    str(self.subnet_mask),
            gateway                =    str(self.gateway),
            dns                    =    str(self.dns),
            hostname               =    str(self.hostname),
            dhcp                   = tobool(self.dhcp),
            hand_comms             = tobool(self.hand_comms),
            hand_power             = tobool(self.hand_power),
            client_connected       = tobool(self.client_connected),
            client_address         =    str(self.client_address),
            request_source_address =    str(self.request_source_address),
        )}


@covvi_message
class DiscoveryResponseMsg(DiscoveryBaseMsg):
    '''A message for unpacking the discovery response from the ECI.'''
    FORMAT_STR = f'{0x8001:016b}' + fStrDiscoResponseBody


@covvi_message
class DiscoveryConfigMsg(DiscoveryBaseMsg):
    '''A message for configuring the discovery parameters of the ECI.'''
    FORMAT_STR = f'{0x045D:016b}' + fStrDiscoResponseBody
