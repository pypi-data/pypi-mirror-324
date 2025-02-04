
from typing import Dict

from eci.utils import leaf_classes
from eci.messages.control_message import ControlMsg
from eci.messages.realtime import ElectrodeValueMsg, DigitStatusMsg, DigitPosnMsg, MotorCurrentMsg, DigitErrorMsg, DigitMoveMsg, CurrentGripMsg
from eci.messages.control import DigitConfigMsg, GripNameMsg, UploadDownLoadMsg
from eci.messages.enums import (
    MessageID, ElectrodeValueMessageID, DigitStatusMessageID, DigitPosnMessageID, MotorCurrentMessageID,
    DigitConfigMessageID, DigitErrorMessageID, GripNameMessageID, DigitMoveMessageID,
)


__to_msg_cls = (lambda msg_cls, msg_enum_cls: {msg_id: msg_cls for msg_id in msg_enum_cls})

_to_msg_cls: Dict[MessageID, ControlMsg] = {
    **{cls.msg_id: cls for cls in leaf_classes(ControlMsg)},
    **__to_msg_cls(ElectrodeValueMsg, ElectrodeValueMessageID),
    **__to_msg_cls(DigitStatusMsg, DigitStatusMessageID),
    **__to_msg_cls(DigitPosnMsg, DigitPosnMessageID),
    **__to_msg_cls(MotorCurrentMsg, MotorCurrentMessageID),
    **__to_msg_cls(DigitConfigMsg, DigitConfigMessageID),
    **__to_msg_cls(DigitErrorMsg, DigitErrorMessageID),
    **__to_msg_cls(GripNameMsg, GripNameMessageID),
    **__to_msg_cls(DigitMoveMsg, DigitMoveMessageID),
    **{
        CurrentGripMsg.msg_id:    CurrentGripMsg,
        UploadDownLoadMsg.msg_id: UploadDownLoadMsg,
    },
}

def to_msg_cls(msg_id: MessageID) -> ControlMsg:
    return _to_msg_cls.get(msg_id)
