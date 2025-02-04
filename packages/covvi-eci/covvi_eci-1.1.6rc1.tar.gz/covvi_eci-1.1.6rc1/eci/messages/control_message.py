
from typing import Iterator, Tuple, Any

from eci.messages.enums import MessageID
from eci.messages.base_message import covvi_message, _n_total_bits
from eci.messages.base_control_message import BaseControlMsg


control_msg_kwargs = set('uid dev_id msg_id cmd_type data_len'.split())


@covvi_message
class ControlMsg(BaseControlMsg):
    FORMAT_STR = BaseControlMsg.FORMAT_STR + '{msg_id:018b}0000{data_len:04b}'
    msg_id:   MessageID = MessageID.nwHandPower
    data_len: int       = 0

    def __post_init__(self):
        super().__post_init__()
        self.msg_id   = MessageID(self.msg_id)
        if self.data_len == 0:
            self.data_len = (_n_total_bits(self.FORMAT_STR) - _n_total_bits(ControlMsg.FORMAT_STR)) // 8

    def __str__(self, table: list = [], width: int = 7) -> str:
        if table:
            return super().__str__(fields=list(self.control_fields)) + '\n'.join([
                ' '.join([f'{str(item):>{width}}' for item in row])
                for row in table
            ]) + '\n'
        else:
            return super().__str__(fields=list(self.fields))

    @property
    def dict(self):
        return {**super().dict, **dict(msg_id=int(self.msg_id))}

    @classmethod
    def unpack(cls, b: bytes):
        msg = super().unpack(b)
        msg.msg_id = MessageID(msg.msg_id)
        return msg

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(**{k:kwargs[k] for k in cls.field_names() if k in kwargs})

    @property
    def args(self) -> Tuple[Any]:
        return tuple(v for k, v in self.fields if k not in control_msg_kwargs)

    @property
    def arg_names(self) -> Tuple[Any]:
        return tuple(k for k, v in self.fields if k not in control_msg_kwargs)

    @property
    def control_fields(self) -> Iterator[Tuple[str, Any]]:
        for i, args in enumerate(self.fields):
            if i == 5:
                break
            yield args


class RealtimeMsg(ControlMsg):
    ...
