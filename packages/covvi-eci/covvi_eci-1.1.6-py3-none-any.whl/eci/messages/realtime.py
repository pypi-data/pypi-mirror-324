
from eci.messages.utils import fStrBits, tobool
from eci.messages.primitives import Percentage, Speed, Int16
from eci.messages.control_message import ControlMsg, RealtimeMsg
from eci.messages.base_message import covvi_message
from eci.messages.enums import (
    MessageID, DigitStatusMessageID, DigitPosnMessageID, DigitMoveMessageID, MotorCurrentMessageID, DigitErrorMessageID,
    CurrentGripID, Table, TableIndex, DirectControlCommand,
)


digit_strings   = 'thumb index middle ring little rotate'
digit_5_strings = 'thumb index middle ring little'
reversed_digit_strings = ' '.join(digit_strings.split()[::-1])
status_strings = 'fault gripping at_open at_posn touch stall stopped active'


@covvi_message
class RealtimeCfgMsg(ControlMsg):
    '''A message for enabling/disabling the receiving of real-time messages.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        fStrBits('digit_error digit_touch motor_current input_status electrode_value current_grip digit_posn digit_status')
    msg_id: MessageID = MessageID.caRealtimeCfg
    digit_error:     bool = False
    digit_touch:     bool = False
    motor_current:   bool = False
    input_status:    bool = False
    electrode_value: bool = False
    current_grip:    bool = False
    digit_posn:      bool = False
    digit_status:    bool = False

    def __post_init__(self):
        super().__post_init__()
        self.digit_error     = tobool(self.digit_error)
        self.digit_touch     = tobool(self.digit_touch)
        self.motor_current   = tobool(self.motor_current)
        self.input_status    = tobool(self.input_status)
        self.electrode_value = tobool(self.electrode_value)
        self.current_grip    = tobool(self.current_grip)
        self.digit_posn      = tobool(self.digit_posn)
        self.digit_status    = tobool(self.digit_status)


@covvi_message
class RealtimeCfg2Msg(ControlMsg):
    '''A message (page 2) for enabling/disabling the receiving of real-time messages.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '00000' + fStrBits('motor_limits orientation environmental')
    msg_id: MessageID = MessageID.caRealtimeCfg2
    motor_limits:  bool = False
    orientation:   bool = False
    environmental: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.motor_limits  = tobool(self.motor_limits)
        self.orientation   = tobool(self.orientation)
        self.environmental = tobool(self.environmental)


@covvi_message
class DigitStatusMsg(ControlMsg):
    '''A message for reading various status parameters of a digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + fStrBits(status_strings)
    msg_id: MessageID = MessageID.caDigitStatus
    fault:    bool = False
    gripping: bool = False
    at_open:  bool = False
    at_posn:  bool = False
    touch:    bool = False
    stall:    bool = False
    stopped:  bool = False
    active:   bool = False

    @property
    def digit_args(m): return m.fault, m.gripping, m.at_open, m.at_posn, m.touch, m.stall, m.stopped, m.active

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(DigitStatusMessageID)
        self.fault    = tobool(self.fault)
        self.gripping = tobool(self.gripping)
        self.at_open  = tobool(self.at_open)
        self.at_posn  = tobool(self.at_posn)
        self.touch    = tobool(self.touch)
        self.stall    = tobool(self.stall)
        self.stopped  = tobool(self.stopped)
        self.active   = tobool(self.active)

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + list(self.arg_names),
            ['args', *self.digit_args],
        ], width=8)


@covvi_message
class DigitStatusAllMsg(RealtimeMsg):
    '''A message for reading various status parameters of all digits.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + fStrBits(digit_strings, status_strings)
    msg_id: MessageID = MessageID.caDigitStatus_all

    thumb_fault:    bool = False
    thumb_gripping: bool = False
    thumb_at_open:  bool = False
    thumb_at_posn:  bool = False
    thumb_touch:    bool = False
    thumb_stall:    bool = False
    thumb_stopped:  bool = False
    thumb_active:   bool = False

    index_fault:    bool = False
    index_gripping: bool = False
    index_at_open:  bool = False
    index_at_posn:  bool = False
    index_touch:    bool = False
    index_stall:    bool = False
    index_stopped:  bool = False
    index_active:   bool = False

    middle_fault:    bool = False
    middle_gripping: bool = False
    middle_at_open:  bool = False
    middle_at_posn:  bool = False
    middle_touch:    bool = False
    middle_stall:    bool = False
    middle_stopped:  bool = False
    middle_active:   bool = False

    ring_fault:    bool = False
    ring_gripping: bool = False
    ring_at_open:  bool = False
    ring_at_posn:  bool = False
    ring_touch:    bool = False
    ring_stall:    bool = False
    ring_stopped:  bool = False
    ring_active:   bool = False

    little_fault:    bool = False
    little_gripping: bool = False
    little_at_open:  bool = False
    little_at_posn:  bool = False
    little_touch:    bool = False
    little_stall:    bool = False
    little_stopped:  bool = False
    little_active:   bool = False

    rotate_fault:    bool = False
    rotate_gripping: bool = False
    rotate_at_open:  bool = False
    rotate_at_posn:  bool = False
    rotate_touch:    bool = False
    rotate_stall:    bool = False
    rotate_stopped:  bool = False
    rotate_active:   bool = False

    @property
    def thumb_args(m): return m.thumb_fault, m.thumb_gripping, m.thumb_at_open, m.thumb_at_posn, m.thumb_touch, m.thumb_stall, m.thumb_stopped, m.thumb_active
    @property
    def index_args(m): return m.index_fault, m.index_gripping, m.index_at_open, m.index_at_posn, m.index_touch, m.index_stall, m.index_stopped, m.index_active
    @property
    def middle_args(m): return m.middle_fault, m.middle_gripping, m.middle_at_open, m.middle_at_posn, m.middle_touch, m.middle_stall, m.middle_stopped, m.middle_active
    @property
    def ring_args(m): return m.ring_fault, m.ring_gripping, m.ring_at_open, m.ring_at_posn, m.ring_touch, m.ring_stall, m.ring_stopped, m.ring_active
    @property
    def little_args(m): return m.little_fault, m.little_gripping, m.little_at_open, m.little_at_posn, m.little_touch, m.little_stall, m.little_stopped, m.little_active
    @property
    def rotate_args(m): return m.rotate_fault, m.rotate_gripping, m.rotate_at_open, m.rotate_at_posn, m.rotate_touch, m.rotate_stall, m.rotate_stopped, m.rotate_active

    @property
    def fault_args(m): return m.thumb_fault, m.index_fault, m.middle_fault, m.ring_fault, m.little_fault, m.rotate_fault
    @property
    def gripping_args(m): return m.thumb_gripping, m.index_gripping, m.middle_gripping, m.ring_gripping, m.little_gripping, m.rotate_gripping
    @property
    def at_open_args(m): return m.thumb_at_open, m.index_at_open, m.middle_at_open, m.ring_at_open, m.little_at_open, m.rotate_at_open
    @property
    def at_posn_args(m): return m.thumb_at_posn, m.index_at_posn, m.middle_at_posn, m.ring_at_posn, m.little_at_posn, m.rotate_at_posn
    @property
    def touch_args(m): return m.thumb_touch, m.index_touch, m.middle_touch, m.ring_touch, m.little_touch, m.rotate_touch
    @property
    def stall_args(m): return m.thumb_stall, m.index_stall, m.middle_stall, m.ring_stall, m.little_stall, m.rotate_stall
    @property
    def stopped_args(m): return m.thumb_stopped, m.index_stopped, m.middle_stopped, m.ring_stopped, m.little_stopped, m.rotate_stopped
    @property
    def active_args(m): return m.thumb_active, m.index_active, m.middle_active, m.ring_active, m.little_active, m.rotate_active

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id == MessageID.caDigitStatus_all
        for digit in 'thumb index middle ring little rotate'.split():
            for attribute in 'fault gripping at_open at_posn touch stall stopped active'.split():
                name = f'{digit}_{attribute}'
                setattr(self, name, tobool(getattr(self, name)))

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + status_strings.split(),
            ['thumb',  *self.thumb_args],
            ['index',  *self.index_args],
            ['middle', *self.middle_args],
            ['ring',   *self.ring_args],
            ['little', *self.little_args],
            ['rotate', *self.rotate_args],
        ], width=8)


@covvi_message
class DigitPosnMsg(ControlMsg):
    '''A message for reading the position of a digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{pos:08b}'
    msg_id: MessageID = MessageID.caDigitPosn
    pos:    int = 0

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(DigitPosnMessageID)
        self.pos = int(self.pos)


@covvi_message
class DigitPosnSetMsg(ControlMsg):
    '''A message for setting the position of a digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + \
        '{speed:08b}00' + fStrBits(reversed_digit_strings) + fStrBits(digit_strings, 'pos', k=8)
    msg_id: MessageID = MessageID.caDigitPosn
    speed:  Speed = Speed(0)
    rotate: bool  = False
    little: bool  = False
    ring:   bool  = False
    middle: bool  = False
    index:  bool  = False
    thumb:  bool  = False
    thumb_pos:  int = 0
    index_pos:  int = 0
    middle_pos: int = 0
    ring_pos:   int = 0
    little_pos: int = 0
    rotate_pos: int = 0

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id == MessageID.caDigitPosn
        self.speed      =  Speed(self.speed)
        self.rotate     = tobool(self.rotate)
        self.little     = tobool(self.little)
        self.ring       = tobool(self.ring)
        self.middle     = tobool(self.middle)
        self.index      = tobool(self.index)
        self.thumb      = tobool(self.thumb)
        self.thumb_pos  =    int(self.thumb_pos)
        self.index_pos  =    int(self.index_pos)
        self.middle_pos =    int(self.middle_pos)
        self.ring_pos   =    int(self.ring_pos)
        self.little_pos =    int(self.little_pos)
        self.rotate_pos =    int(self.rotate_pos)


@covvi_message
class DigitPosnAllMsg(RealtimeMsg):
    '''A message for reading the position of all digits.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + fStrBits(digit_strings, 'pos', k=8)
    msg_id: MessageID = MessageID.caDigitPosn_all
    thumb_pos:  int = 0
    index_pos:  int = 0
    middle_pos: int = 0
    ring_pos:   int = 0
    little_pos: int = 0
    rotate_pos: int = 0

    @property
    def position_args(m): return m.thumb_pos, m.index_pos, m.middle_pos, m.ring_pos, m.little_pos, m.rotate_pos

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id == MessageID.caDigitPosn_all
        self.thumb_pos  = int(self.thumb_pos)
        self.index_pos  = int(self.index_pos)
        self.middle_pos = int(self.middle_pos)
        self.ring_pos   = int(self.ring_pos)
        self.little_pos = int(self.little_pos)
        self.rotate_pos = int(self.rotate_pos)

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + digit_strings.split(),
            ['position', *self.position_args],
        ], width=9)


@covvi_message
class CurrentGripMsg(RealtimeMsg):
    '''A message for reading the current grip of the hand.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + '{grip_id:08b}{table:04b}{table_index:04b}'
    msg_id: MessageID = MessageID.caCurrentGrip
    grip_id:     CurrentGripID = CurrentGripID.TRIPOD_OPEN
    table:       Table         = Table.A
    table_index: TableIndex    = TableIndex.I0

    def __post_init__(self):
        super().__post_init__()
        self.grip_id     = CurrentGripID(int(self.grip_id))
        self.table       = Table(int(self.table))
        self.table_index = TableIndex(int(self.table_index))


@covvi_message
class CurrentGripGripIdMsg(ControlMsg):
    '''A message for setting the current grip of the hand via grip ID.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{grip_id:08b}'
    msg_id: MessageID = MessageID.caCurrentGrip
    grip_id: CurrentGripID = CurrentGripID.TRIPOD_OPEN
    data_len: int = 1

    def __post_init__(self):
        super().__post_init__()
        self.grip_id = CurrentGripID(int(self.grip_id))


@covvi_message
class CurrentGripTableMsg(ControlMsg):
    '''A message for setting the current grip of the hand via table and table index.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '0'*8 + '{table:04b}{table_index:04b}'
    msg_id: MessageID = MessageID.caCurrentGrip
    table:       Table      = Table.A
    table_index: TableIndex = TableIndex.I0
    data_len: int = 2

    def __post_init__(self):
        super().__post_init__()
        self.table       = Table(int(self.table))
        self.table_index = TableIndex(int(self.table_index))


@covvi_message
class ElectrodeValueMsg(RealtimeMsg):
    '''A message for reading the electrode value of A or B.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + '{voltage:016b}'
    msg_id: MessageID = MessageID.caElectrodeValue
    voltage: Int16 = Int16(0)

    @property
    def a_or_b(self) -> str:
        return self.msg_id - MessageID.caElectrodeValue

    def __post_init__(self):
        super().__post_init__()
        self.voltage = Int16(self.voltage)

    def __str__(self) -> str:
        return super().__str__(table=f'''
{'AB'[self.a_or_b] = }
{self.voltage  = }
'''.split('\n'), width=7)


@covvi_message
class DirectControlMsg(ControlMsg):
    '''A message for opening/closing the hand.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{command:08b}{speed:08b}'
    msg_id: MessageID = MessageID.caDirectControl
    command: int   = 0
    speed:   Speed = Speed(0)

    def __post_init__(self):
        super().__post_init__()
        self.command = int(self.command)
        assert self.command in set(DirectControlCommand)
        self.speed = Speed(value=self.speed)


@covvi_message
class DigitMoveMsg(ControlMsg):
    '''A message for moving a digit of the hand.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{position:08b}{speed:08b}{power:08b}{limit:08b}'
    msg_id: MessageID = MessageID.caDigitMove
    position: int        = 0
    speed:    Speed      = Speed(0)
    power:    Percentage = Percentage(Percentage.MIN)
    limit:    Percentage = Percentage(Percentage.MIN)

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(DigitMoveMessageID)
        self.position = int(self.position)
        self.speed    = Speed(self.speed)
        self.power    = Percentage(self.power)
        self.limit    = Percentage(self.limit)
        assert self.position in range(0xFF + 1)


@covvi_message
class InputStatusMsg(RealtimeMsg):
    '''A message for reading the input status of the hand.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + \
        '{supinate:01b}{pronate:01b}{back_button:01b}{little_tip:01b}{ring_tip:01b}{middle_tip:01b}{index_tip:01b}{thumb_tip:01b}'
    msg_id: MessageID = MessageID.caInputStatus
    supinate:    bool = False
    pronate:     bool = False
    back_button: bool = False
    little_tip:  bool = False
    ring_tip:    bool = False
    middle_tip:  bool = False
    index_tip:   bool = False
    thumb_tip:   bool = False

    def __post_init__(self):
        super().__post_init__()
        self.supinate    = tobool(self.supinate)
        self.pronate     = tobool(self.pronate)
        self.back_button = tobool(self.back_button)
        self.little_tip  = tobool(self.little_tip)
        self.ring_tip    = tobool(self.ring_tip)
        self.middle_tip  = tobool(self.middle_tip)
        self.index_tip   = tobool(self.index_tip)
        self.thumb_tip   = tobool(self.thumb_tip)


@covvi_message
class MotorCurrentMsg(ControlMsg):
    '''A message for reading the motor current of a digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '{current:08b}'
    msg_id: MessageID = MessageID.caMotorCurrent
    current: int = 0

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(MotorCurrentMessageID)
        self.current = int(self.current)


@covvi_message
class MotorCurrentAllMsg(RealtimeMsg):
    '''A message for reading the motor current of all digits.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + fStrBits(digit_5_strings, 'current', k=8)
    msg_id: MessageID = MessageID.caMotorCurrent_all
    thumb_current:  int = 0
    index_current:  int = 0
    middle_current: int = 0
    ring_current:   int = 0
    little_current: int = 0

    @property
    def current_args(m): return m.thumb_current, m.index_current, m.middle_current, m.ring_current, m.little_current

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id == MessageID.caMotorCurrent_all
        self.thumb_current  = int(self.thumb_current)
        self.index_current  = int(self.index_current)
        self.middle_current = int(self.middle_current)
        self.ring_current   = int(self.ring_current)
        self.little_current = int(self.little_current)

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + digit_5_strings.split(),
            ['current', *self.current_args],
        ], width=8)


@covvi_message
class DigitErrorMsg(ControlMsg):
    '''A message for reading the error status of a digit.'''
    FORMAT_STR = ControlMsg.FORMAT_STR + '0000{position:01b}{limits:01b}{motor:01b}{hall:01b}'
    msg_id: MessageID = MessageID.caDigitError
    position: bool = False
    limits:   bool = False
    motor:    bool = False
    hall:     bool = False

    def __post_init__(self):
        super().__post_init__()
        assert self.msg_id in set(DigitErrorMessageID)
        self.position = tobool(self.position)
        self.limits   = tobool(self.limits)
        self.motor    = tobool(self.motor)
        self.hall     = tobool(self.hall)


@covvi_message
class DigitTouchAllMsg(RealtimeMsg):
    '''A message for reading the touch status of all digits.'''
    FORMAT_STR = RealtimeMsg.FORMAT_STR + fStrBits(digit_5_strings, 'touch', k=8)
    msg_id: MessageID = MessageID.caDigitTouch_all
    thumb_touch:  int = 0
    index_touch:  int = 0
    middle_touch: int = 0
    ring_touch:   int = 0
    little_touch: int = 0

    @property
    def touch_args(m): return m.thumb_touch, m.index_touch, m.middle_touch, m.ring_touch, m.little_touch

    def __post_init__(self):
        super().__post_init__()
        self.thumb_touch  = int(self.thumb_touch)
        self.index_touch  = int(self.index_touch)
        self.middle_touch = int(self.middle_touch)
        self.ring_touch   = int(self.ring_touch)
        self.little_touch = int(self.little_touch)

    def __str__(self) -> str:
        return super().__str__(table=[
            [''] + digit_5_strings.split(),
            ['touch', *self.touch_args],
        ], width=8)
