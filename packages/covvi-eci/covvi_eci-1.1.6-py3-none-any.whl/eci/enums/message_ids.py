
from eci.enums.enums import Firmware, Digit, Digit5, ElectrodeValue, GripNameIndex, BaseIntEnum


ALL_OFFSET        = 0xF
CLEAR_CONFIG_BYTE = 0x5A


class BaseMessageID(BaseIntEnum):
    ...


class FirmwareMessageID(BaseMessageID):
    caFirmware = 0x00050 # Device Firmware
    (
        caFirmware_PIC, caFirmware_FPGA, caFirmware_BLE, caFirmware_FRAM, caFirmware_MAX,
    ) = range(caFirmware, caFirmware + len(Firmware))


class DigitStatusMessageID(BaseMessageID):
    caDigitStatus = 0x00110 # Digit status flags
    (
        caDigitStatus_thumb, caDigitStatus_index, caDigitStatus_middle, caDigitStatus_ring, caDigitStatus_little, caDigitStatus_rotate,
    ) = range(caDigitStatus, caDigitStatus + len(Digit))


class DigitPosnMessageID(BaseMessageID):
    caDigitPosn = 0x00120 # Digit position
    (
        caDigitPosn_thumb, caDigitPosn_index, caDigitPosn_middle, caDigitPosn_ring, caDigitPosn_little, caDigitPosn_rotate,
    ) = range(caDigitPosn, caDigitPosn + len(Digit))


class ElectrodeValueMessageID(BaseMessageID):
    caElectrodeValue = 0x00140 # Electrode value
    (
        caElectrodeValue_a, caElectrodeValue_b
    ) = range(caElectrodeValue, caElectrodeValue + len(ElectrodeValue))


class DigitMoveMessageID(BaseMessageID):
    caDigitMove = 0x00160 # Command to move a single digit
    (
        caDigitMove_thumb, caDigitMove_index, caDigitMove_middle, caDigitMove_ring, caDigitMove_little, caDigitMove_rotate,
    ) = range(caDigitMove, caDigitMove + len(Digit))


class MotorCurrentMessageID(BaseMessageID):
    caMotorCurrent = 0x00180 # Motor current
    (
        caMotorCurrent_thumb, caMotorCurrent_index, caMotorCurrent_middle, caMotorCurrent_ring, caMotorCurrent_little,
    ) = range(caMotorCurrent, caMotorCurrent + len(Digit5))


class DigitErrorMessageID(BaseMessageID):
    caDigitError = 0x00190 # Digit error flags
    (
        caDigitError_thumb, caDigitError_index, caDigitError_middle, caDigitError_ring, caDigitError_little, caDigitError_rotate,
    ) = range(caDigitError, caDigitError + len(Digit))


class DigitConfigMessageID(BaseMessageID):
    caDigitConfig = 0x00200 # Configure digit limits
    (
        caDigitConfig_thumb, caDigitConfig_index, caDigitConfig_middle, caDigitConfig_ring, caDigitConfig_little, caDigitConfig_rotate,
    ) = range(caDigitConfig, caDigitConfig + len(Digit))


class GripNameMessageID(BaseMessageID):
    caGripName = 0x00320 # Installed user grips
    (
        caGripName_0, caGripName_1, caGripName_2, caGripName_3, caGripName_4, caGripName_5
    ) = range(caGripName, caGripName + len(GripNameIndex))


class MessageID(BaseMessageID):

    def __add__(self, __value: int) -> int:
        return MessageID(int(self) + int(__value))

    def __radd__(self, __value: int) -> int:
        return self.__add__(__value)

    ################################################################
    # Hand power
    ################################################################

    nwHandPower  = 0x00F00 # Power on/off the hand
    nwDeviceInfo = 0x00F10 # Device info for each CanBUS device

    ################################################################
    # Discovery and device messages
    ################################################################

    caWake            = 0x00000 # 
    caDisco           = 0x00010 # 
    caHello           = 0x00020 # 
    caLeave           = 0x00030 # Leave bus
    caSerialNumber    = 0x00040 # Device serial number
    caFirmware        = 0x00050 # Device firmware
    (
        caFirmware_PIC, caFirmware_FPGA, caFirmware_BLE, caFirmware_FRAM, caFirmware_MAX,
    ) = list(FirmwareMessageID)
    caFactoryDefaults = 0x00060 # Restore factory defaults
    caDeviceIdentity  = 0x00070 # Device identity parameters
    caDeviceProduct   = 0x00080 # Product and manufacturer
    caDeviceMacAddr   = 0x00090 # Device MAC address
    caBleSettings     = 0x000A0 # Bluetooth settings
    caBleAttributes   = 0x000B0 # Bluetooth attributes
    caRegistration    = 0x000C0 # Registration timestamp
    # caBusMember       = 0x000D0 # CANbus members

    ################################################################
    # Real-time messages
    ################################################################

    caRealtimeCfg       = 0x00100 # Real-time update configuration
    caRealtimeCfg2      = 0x00101 # Real-time update configuration (page2)
    caDigitStatus       = 0x00110 # Digit status flags
    (
        caDigitStatus_thumb, caDigitStatus_index, caDigitStatus_middle, caDigitStatus_ring, caDigitStatus_little, caDigitStatus_rotate,
    ) = list(DigitStatusMessageID)
    caDigitStatus_all   = caDigitStatus + ALL_OFFSET # Digit status flags (all statuses)
    caDigitPosn         = 0x00120 # Digit position
    (
        caDigitPosn_thumb, caDigitPosn_index, caDigitPosn_middle, caDigitPosn_ring, caDigitPosn_little, caDigitPosn_rotate,
    ) = list(DigitPosnMessageID)
    caDigitPosn_all     = caDigitPosn + ALL_OFFSET # Digit position (all positions)
    caCurrentGrip       = 0x00130 # Current grip
    caElectrodeValue    = 0x00140 # Electrode value
    (
        caElectrodeValue_a, caElectrodeValue_b
    ) = list(ElectrodeValueMessageID)
    caDirectControl     = 0x00150 # Direct open & close command
    caDigitMove         = 0x00160 # Command to move a single digit
    (
        caDigitMove_thumb, caDigitMove_index, caDigitMove_middle, caDigitMove_ring, caDigitMove_little, caDigitMove_rotate,
    ) = list(DigitMoveMessageID)
    caInputStatus       = 0x00170 # State of trigger inputs
    caMotorCurrent      = 0x00180 # Motor current
    (
        caMotorCurrent_thumb, caMotorCurrent_index, caMotorCurrent_middle, caMotorCurrent_ring, caMotorCurrent_little,
    ) = list(MotorCurrentMessageID)
    caMotorCurrent_all  = caMotorCurrent + ALL_OFFSET # Motor current (all currents)
    caDigitError        = 0x00190 # Digit error flags
    (
        caDigitError_thumb, caDigitError_index, caDigitError_middle, caDigitError_ring, caDigitError_little, caDigitError_rotate,
    ) = list(DigitErrorMessageID)
    caVoltageMonitor    = 0x001A0 # Motor voltage monitor
    caDigitTouch        = 0x001B0 # Request digit status
    caDigitTouch_all  = caDigitTouch + ALL_OFFSET # Request digit status (all statuses)

    ################################################################
    # Digit configuration messages
    ################################################################

    caDigitConfig       = 0x00200 # Configure digit limits
    (
        caDigitConfig_thumb, caDigitConfig_index, caDigitConfig_middle, caDigitConfig_ring, caDigitConfig_little, caDigitConfig_rotate,
    ) = list(DigitConfigMessageID)
    caPinchConfig       = 0x00210 # Configure pinch points
    caDigitReference    = 0x00220 # Configure digit reference points
    caHapticConfig      = 0x00230 # Configure haptic feedback response
    caCalibrationBackup = 0x002F0 # Backup/Restore calibration parameters
    #caCalibrationData   = 0x002F0

    ################################################################
    # Grip configuration messages
    ################################################################

    caGripTable         = 0x00300 # Configure grip tables
    caGripModes         = 0x00310 # Configure grip options
    # caGripMode          = 0x00310
    caGripName          = 0x00320 # Installed user grips
    (
        caGripName_0, caGripName_1, caGripName_2, caGripName_3, caGripName_4, caGripName_5
    ) = list(GripNameMessageID)
    caGripPowerCal      = 0x00330 # Grip power calibration

    ################################################################
    # Grip trigger configuration
    ################################################################

    caTriggerAction     = 0x00400 # Configure trigger actions
    caTriggerTime       = 0x00410 # Configure trigger times
    caTriggerEvent      = 0x00420 # Trigger event
    caTriggerMapGrip    = 0x00440 # Configure map to grip
    caTriggerThreshold  = 0x00450 # Trigger threshold for touch sensors

    ################################################################
    # Electrode configuration
    ################################################################

    caElectrodeRange    = 0x00500 # Configure limits for electrodes
    caElectrodeThresh   = 0x00510 # Threshold levels
    caElectrodeCocon    = 0x00520 # Cocontraction levels

    ################################################################
    # Mode configuration
    ################################################################

    caModeConfig        = 0x00600 # Operating mode configuration
    caModeTime          = 0x00610 # Grip switch times etc.

    ################################################################
    # System and status messages
    ################################################################

    caUserInterface     = 0x00700 # Screen,Buzzer,Vibration
    caEnvironmental     = 0x00710 # Read temperature, battery voltage etc
    caSystemStatus      = 0x00720 # Read system status
    caOrientation       = 0x00730 # Hand orientation
    caUserStandby       = 0x00740 # Standby mode
    caDisplayPosition   = 0x00750 # Dorsal screen display offsets
    caHandName          = 0x00760 # Hand Name
    caMotorLimits       = 0x00770 # Motor Limits

    ################################################################
    # Peripheral configuration
    ################################################################

    caRemoteConfig		= 0x00800

    ################################################################
    # Statistics and errors
    ################################################################

    caStatistics        = 0x00A00 # Download statistics
    caErrorLog          = 0x00A10 # Download error log

    ################################################################
    # Firmware update messages
    ################################################################

    caUpdateDownload    = 0x00C00 # Download firmware to hand
    caUpdateFileInfo    = 0x00C10 # Information for stored update files
    caUpdateProgram     = 0x00C20 # Program with downloaded firmware
    caUpdateError       = 0x00C30 # Get error code(s) for update failure
    caUpdateHexParam    = 0x00C40 # Set hex record parameters
    caUpdateBle         = 0x00C50 # Bluetooth module update

    ################################################################
    # Factory test messages
    ################################################################

    caDispatch          = 0x00E00 # Configure device for Shipment
    caSpeedTest         = 0x00E10 # Perform digit speed test
    caTestMode          = 0x00E20 # Configure test mode
    caTestFunction      = 0x00E30 # Perform test function
    caPdiTestInfo       = 0x00E40 # PDI test information
    caClearConfig       = 0x00E50 # Clear all config data in FRAM
