
from typing import Union, Type, Dict
from enum import EnumMeta, Enum, IntEnum
from random import choice


NET_UID       = 'V'
UID_DELIMITER = bytes([ord(NET_UID)])


class DefaultEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultEnumMeta.default:
            # Assume the first enum is default
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)


class BaseEnum(Enum, metaclass=DefaultEnumMeta):
    @classmethod
    def random(cls):
        return choice(list(cls))


class BaseStrEnum(BaseEnum):
    def __str__(self) -> str:
        return str(self.value)


class BaseIntEnum(IntEnum, BaseEnum):
    def __format__(self, format_string: str) -> str:
        if format_string:
            return super().__format__(format_string)
        else:
            return self.name


class CommandString(BaseStrEnum):
    ...


class CommandCode(BaseIntEnum):
    RTD, BLK, CMD, RTR, RES = 0x08, 0x04, 0x02, 0x01, 0x00
    BLK_RTR = BLK | RTR

    def str(self) -> CommandString:
        return {i:s for i, s in zip(CommandCode, CommandString)}[self]


class CommandString(BaseStrEnum):
    RTD, BLK, CMD, RTR, RES = 'RTD BLK CMD RTR RES'.split()
    BLK_RTR = f'{BLK} & {RTR}'

    def int(self) -> CommandCode:
        return {s:i for s, i in zip(CommandString, CommandCode)}[self]


class NetDevice(BaseIntEnum):
    D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, DA, DB, DC, DD, DE, DF = range(0x10)
    LOCAL, HAND = D0, D1


class DirectControlCommand(BaseIntEnum):
    STOP, OPEN, CLOSE = range(3)


class GripNameIndex(BaseIntEnum):
    GN0, GN1, GN2, GN3, GN4, GN5 = range(6)


class BuiltinGripID(BaseIntEnum):
    _NO_GRIP, TRIPOD, POWER, TRIGGER, PREC_OPEN, PREC_CLOSED, KEY, FINGER, CYLINDER, COLUMN, RELAXED, GLOVE, TAP, GRAB, TRIPOD_OPEN = range(15)


class CurrentGripID(BaseIntEnum):
    _NO_GRIP, TRIPOD, POWER, TRIGGER, PREC_OPEN, PREC_CLOSED, KEY, FINGER, CYLINDER, COLUMN, RELAXED, GLOVE, TAP, GRAB, TRIPOD_OPEN = range(len(BuiltinGripID))
    GN0, GN1, GN2, GN3, GN4, GN5 = range(len(BuiltinGripID), len(BuiltinGripID) + len(GripNameIndex))


class UserGripID(BaseIntEnum):
    FIST, HOOK, PRECISION_HALF, RIPPLE, STICK_IT, THUMBS_UP, TRIPOD_CLOSED, TRIPOD_OPEN, TWO_FINGERS, WAVE = range(10)


class Table(BaseIntEnum):
    A, B, C, D = range(4)


class TableIndex(BaseIntEnum):
    I0, I1, I2, I3, I4, I5 = range(6)


class DeviceClass(BaseIntEnum):
    (
        NONE,
        HAND,    # Hand Device Class
        TEST,    # Test System Device Class
        INPUT,   # Input Device, Electrodes ETC
        OUTPUT,  # Output Device, Display ETC
    ) = range(5)


class DeviceHandType(BaseIntEnum):
    (
        NONE, _,
        SMALL_LEFT_HAND, SMALL_RIGHT_HAND,
        MEDIUM_LEFT_HAND, MEDIUM_RIGHT_HAND,
        LARGE_LEFT_HAND, LARGE_RIGHT_HAND
    ) = range(7 + 1)


class DeviceTestType(BaseIntEnum):
    (
        SYSTEM, # System Test Station
        PTEST,  # Peripheral Test Unit
    ) = range(1, 2 + 1)


class DeviceInputType(BaseIntEnum):
    (
        ELECT, # Electrode
        SDU,   # Sales Demo Unit
        PRS,   # Pattern Recognition System
        ROS,   # RoS Interface
        RCI,   # Remote Control Interface
        ECI,   # Ethernet Control Interface
    ) = range(1, 6 + 1)


class DeviceOutputType(BaseIntEnum):
    (
        WRIST,  # Wrist Rotator
        HAPTIC, # Haptic Transducer
    ) = range(1, 2 + 1)


def make_class_type(device_class: int, device_type: int) -> int:
    return ((device_class & 0xF) << 4) + ((device_type & 0xF) << 0)


class DeviceClassType(BaseIntEnum):
    NONE = 0
    _1, _2, SMALL_LEFT_HAND, SMALL_RIGHT_HAND, MEDIUM_LEFT_HAND, MEDIUM_RIGHT_HAND, LARGE_LEFT_HAND, LARGE_RIGHT_HAND = [
        make_class_type(DeviceClass.HAND, i) for i in list(DeviceHandType)
    ]
    SYSTEM, PTEST = [
        make_class_type(DeviceClass.TEST, i) for i in list(DeviceTestType)
    ]
    ELECT, SDU, PRS, ROS, RCI, ECI = [
        make_class_type(DeviceClass.INPUT, i) for i in list(DeviceInputType)
    ]
    WRIST, HAPTIC = [
        make_class_type(DeviceClass.OUTPUT, i) for i in list(DeviceOutputType)
    ]

    @property
    def device_class_type(self, _device_class_type_mapping: Dict[DeviceClass, Type[BaseIntEnum]]={
            DeviceClass.HAND:   DeviceHandType,
            DeviceClass.TEST:   DeviceTestType,
            DeviceClass.INPUT:  DeviceInputType,
            DeviceClass.OUTPUT: DeviceOutputType,
        }) -> Union[DeviceHandType, DeviceTestType, DeviceInputType, DeviceOutputType]:
        device_class = DeviceClass((int(self) >> 4) & 0xF)
        return device_class, _device_class_type_mapping[device_class]((int(self) >> 0) & 0xF)


class DeviceGlove(BaseIntEnum):
    CLEAR, BLACK = range(2)


class DeviceColour(BaseIntEnum):
    WHITE, CARBON, ROSE_GOLD, TITAN_GRAY = range(4)


class Language(BaseIntEnum):
    ENGLISH, GERMAN, SPANISH, FRENCH, ITALIAN, DUTCH = range(6)


class Digit5(BaseIntEnum):
    THUMB, INDEX, MIDDLE, RING, LITTLE = range(5)


class Digit(BaseIntEnum):
    (THUMB, INDEX, MIDDLE, RING, LITTLE), THUMB_ROTATION = list(Digit5), 5


class ElectrodeValue(BaseIntEnum):
    A, B = range(2)


class Firmware(BaseIntEnum):
    PIC, FPGA, BLE, FRAM, MAX = range(5)


class ProductString(BaseStrEnum):
    ...


class ProductID(BaseIntEnum):
    NONE = 0x00

    # Product IDs (Covvi)
    NEXUS     = 0x11 # Nexus Hand
    COVVICAN  = 0x12 # CovviCan
    HAPTIC    = 0x13 # Haptic Feedback Module
    REMOTE    = 0x14 # Remote Control Interface
    PERI_TEST = 0x15 # Peripheral Test Box
    ECI       = 0x16 # Ethernet Control Interface

    # Product IDs (Coapt)
    GEN2 = 0x21 # Gen2 Pattern Recognition System

    # 
    GLIDE = 0x31 # Glide
    ADAPT = 0x32 # Sense Adapt

    # Product IDs (TKE)
    ROS = 0x41 # RoS interface

    def str(self) -> ProductString:
        return {i:s for i, s in zip(ProductID, ProductString)}[self]


class ProductString(BaseStrEnum):
    NONE          = f'NONE [{int(ProductID.NONE)}]'

    # Product IDs (Covvi)
    NEXUS     = f'NEXUS_HAND [{int(ProductID.NEXUS)}]'
    COVVICAN  = f'COVVICAN [{int(ProductID.COVVICAN)}]'
    HAPTIC    = f'HAPTIC [{int(ProductID.HAPTIC)}]'
    REMOTE    = f'REMOTE [{int(ProductID.REMOTE)}]'
    PERI_TEST = f'PERI_TEST [{int(ProductID.PERI_TEST)}]'
    ECI       = f'ECI [{int(ProductID.ECI)}]'

    # Product IDs (Coapt)
    GEN2 = f'GEN2 [{int(ProductID.GEN2)}]'

    # 
    GLIDE = f'GLIDE [{int(ProductID.GLIDE)}]'
    ADAPT = f'ADAPT [{int(ProductID.ADAPT)}]'

    # Product IDs (TKE)
    ROS = f'ROS [{int(ProductID.ROS)}]'

    def int(self) -> ProductID:
        return {s:i for s, i in zip(ProductString, ProductID)}[self]


class BulkDataType(BaseIntEnum):
    RESET = 0x0 # finish or abort file transfer
    FW    = 0x1 # hex byte code file
    GW    = 0x2 # standard jbc file
    GRIP  = 0x3 # user grip file


class UpdateStatus(BaseIntEnum):
    (
        Ok,                 # update process OK
	    Erasing,            # erasing flash
	    BlankCheck,         # blank checking flash
	    EraseFailure,       # failed to erase external flash
	    EraseComplete,      # successfully erased flash
	    TransferFailure,    # failed to transfer file to flash
	    TransferComplete,   # successfully wrote file to flash
	    ValidationRunning,  # file validation in progress
	    ValidationStalled,  # file validation stalled
	    ValidationComplete, # file validation completed
	    ValidationError,    # file validation error
	    ProgramStarted,     # reprogramming started
	    ProgramDSM,         # reprogramming DSM
	    ProgramCFM0_3,      # reprogramming CFM at sector 3
	    ProgramCFM0_4,      # reprogramming CFM at sector 4
	    ProgramCFM0_5,      # reprogramming CFM at sector 5
	    ProgramUFM_1,       # reprogramming UFM at sector 1
	    ProgramUFM_2,       # reprogramming UFM at sector 2
	    ProgramStalled,     # reprogramming process stalled
	    StartBootloader,    # starting bootloader
	    ProgramComplete,    # reprogramming completed
	    ProgramAborted,     # reprogramming aborted
	    ProgramError,       # reprogramming error
    ) = range(23)
