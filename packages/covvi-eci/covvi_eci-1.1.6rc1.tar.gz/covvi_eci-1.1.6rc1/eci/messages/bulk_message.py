
from eci.messages.primitives import Command
from eci.messages.enums import CommandCode
from eci.messages.base_message import covvi_message
from eci.messages.base_control_message import BaseControlMsg


@covvi_message
class BulkMsg(BaseControlMsg):
    FORMAT_STR = BaseControlMsg.FORMAT_STR + '{block_index:018b}0000'
    block_index: int = 0


@covvi_message
class BulkRequestMsg(BulkMsg):
    '''A message for unpacking a bulk request from the hand.'''
    FORMAT_STR = BulkMsg.FORMAT_STR + '0000'
    cmd_type: Command = Command(CommandCode.BLK_RTR)

    @property
    def dict(self):
        return {**super().dict, **dict(cmd_type=int(self.cmd_type))}


@covvi_message
class BulkResponseMsg(BulkMsg):
    '''A message for responding to a bulk request from the hand.'''
    FORMAT_STR = BulkMsg.FORMAT_STR + '{data_len:04b}' + ''.join([f'{{byte{i+1}:08b}}' for i in range(8)])
    cmd_type: Command = Command(CommandCode.BLK)
    data_len: int = 0
    byte1:    int = 0
    byte2:    int = 0
    byte3:    int = 0
    byte4:    int = 0
    byte5:    int = 0
    byte6:    int = 0
    byte7:    int = 0
    byte8:    int = 0

    @property
    def dict(self):
        return {**super().dict, **dict(cmd_type=int(self.cmd_type))}

    @classmethod
    def from_bytes(cls, block_index: int, b: bytes):
        return BulkResponseMsg(data_len=len(b), block_index=block_index,
            **{byte_name: byte for byte_name, byte in zip([f'byte{i+1}' for i in range(8)], b)}
        )
