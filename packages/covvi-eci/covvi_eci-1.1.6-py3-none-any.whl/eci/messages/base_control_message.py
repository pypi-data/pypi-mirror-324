
from eci.messages.primitives import Command
from eci.messages.enums import NET_UID, NetDevice, CommandCode
from eci.messages.base_message import BaseMessage, covvi_message


@covvi_message
class BaseControlMsg(BaseMessage):
    FORMAT_STR = BaseMessage.FORMAT_STR + '{uid:08b}0000{dev_id:04b}00{cmd_type:04b}'
    uid:      str       = NET_UID
    dev_id:   NetDevice = NetDevice.HAND
    cmd_type: Command   = Command(CommandCode.CMD)

    def __post_init__(self):
        super().__post_init__()
        if type(self.dev_id) is int:
            self.dev_id = NetDevice(self.dev_id)
        self.cmd_type = Command(self.cmd_type)

    @property
    def dict(self):
        return {**super().dict, **dict(dev_id=int(self.dev_id), cmd_type=int(self.cmd_type))}

    def pack(self, *args, **kwargs) -> bytes:
        return super().pack(
            *args,
            uid = ord(self.uid) & 0xFF,
            **kwargs,
        )

    @classmethod
    def unpack(cls, b: bytes):
        msg = super().unpack(b)
        assert msg.uid == ord(NET_UID) # V 0x56 01010110
        msg.uid = chr(msg.uid)
        msg.dev_id = NetDevice(msg.dev_id)
        return msg
