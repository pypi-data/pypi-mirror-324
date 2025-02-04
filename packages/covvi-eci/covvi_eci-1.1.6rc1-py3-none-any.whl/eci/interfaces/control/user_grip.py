
from time import sleep
from logging import debug
import importlib.resources
from pathlib import Path
from typing import Union, List

from eci.utils import VERSION, VERSION_3_10
from eci.interfaces.utils import public
from eci.interfaces.control.base_control_interface import BaseControlInterface
from eci.interfaces.primitives import GripName, BulkBytes, CurrentGrip, Command, FourOctetAddress
from eci.interfaces.enums import (
    GripNameIndex, UpdateStatus, CurrentGripID, UserGripID, NetDevice, Table, TableIndex, CommandCode,
)
from eci.interfaces.messages import (
    ControlMsg, SendUserGripCmdMsg, RemoveUserGripCmdMsg, BulkRequestMsg, BulkResponseMsg, UserGripResMsg, GripNameMsg,
    CurrentGripMsg, CurrentGripGripIdMsg, CurrentGripTableMsg,
)


USER_GRIPS_DIR     = 'grips'
USER_GRIP_FILE_EXT = 'gbc'


if VERSION < VERSION_3_10:
    _user_grip_to_path_map = {
        _user_grip.value: path
        for _user_grip in UserGripID
        for context_manager in [importlib.resources.path(
            USER_GRIPS_DIR,
            f'''{_user_grip.name.lower().replace('_', ' ')}.{USER_GRIP_FILE_EXT}''',
        )]
        for path in [str(context_manager.__enter__())]
        for _ in [context_manager.__exit__(None, None, None)]
    }

elif VERSION == VERSION_3_10:
    _user_grip_to_path_map = {
        _user_grip.value: str(importlib.resources.path(
            USER_GRIPS_DIR,
            f'''{_user_grip.name.lower().replace('_', ' ')}.{USER_GRIP_FILE_EXT}''',
        ))
        for _user_grip in UserGripID
    }

elif VERSION > VERSION_3_10:
    _user_grip_to_path_map = {
        _user_grip.value: str(importlib.resources.files(USER_GRIPS_DIR).joinpath(
            f'''{_user_grip.name.lower().replace('_', ' ')}.{USER_GRIP_FILE_EXT}'''
        ))
        for _user_grip in UserGripID
    }

else:
    raise Exception(f''''_user_grip_to_path_map' in {VERSION = }, is not handled properly.''')


class UserGripInterface(BaseControlInterface):
    '''An interface to perform user grip operations: sending a user grip to the hand, removing a user grip from the hand, and resetting the user grips.'''

    cUserGripKey = 'GRIP'.encode()

    def __init__(self, host: Union[str, FourOctetAddress]):
        debug('Initializing the user grip interface.')
        super().__init__(host)
        self._reset_bulk_transfer_state()
        self._message_dict[BulkRequestMsg] = self._process_BulkRequestMsg
        debug('Initialized the user grip interface.')

    def __enter__(self):
        debug('Starting the user grip interface.')
        super().__enter__()
        self._reset_bulk_transfer_state()
        debug('Started the user grip interface.')
        return self

    def __exit__(self, *args):
        debug('Closing the user grip interface.')
        self._reset_bulk_transfer_state()
        super().__exit__()
        debug('Closed the user grip interface.')

    ################################################################

    def _reset_bulk_transfer_state(self) -> None:
        self._file_bytes = BulkBytes(b'\x00' * 16)
        self._total_bytes_sent = 0

    def _process_BulkRequestMsg(self, msg: BulkRequestMsg) -> None:
        block_bytes = self._file_bytes.get_block(msg.block_index)
        self._send(BulkResponseMsg.from_bytes(msg.block_index, block_bytes))
        self._total_bytes_sent = self._total_bytes_sent + len(block_bytes)

    ################################################################

    def _user_grip_to_path(self, user_grip: UserGripID) -> Path:
        return _user_grip_to_path_map[user_grip]

    def _getGripFileBytes(self, file_path: str) -> BulkBytes:
        with open(file_path, 'rb') as file:
            file_bytes = BulkBytes(file.read())
        assert file_bytes.startswith(UserGripInterface.cUserGripKey)
        return file_bytes

    def _performUserGripErasing(self) -> BulkRequestMsg:
        msg1 = self._get_message(UserGripResMsg)
        assert type(msg1) is UserGripResMsg
        assert msg1.update_status == UpdateStatus.Erasing

        msg2 = self._get_message(UserGripResMsg)
        assert type(msg2) is UserGripResMsg
        assert msg2.update_status == UpdateStatus.EraseComplete

        return msg1, msg2

    ################################################################

    @public
    def sendUserGrip(self, grip_name_index: GripNameIndex, user_grip: UserGripID) -> UserGripResMsg:
        self._reset_bulk_transfer_state()
        self._file_bytes = file_bytes = self._getGripFileBytes(self._user_grip_to_path(user_grip))
        self._send(SendUserGripCmdMsg(grip_name_index=grip_name_index, file_len=len(file_bytes), major_version=file_bytes[4], minor_version=file_bytes[5]))
        msg1, msg2 = self._performUserGripErasing()
        msg: UserGripResMsg = self._get_message(UserGripResMsg)
        assert msg.update_status == UpdateStatus.TransferComplete
        assert self._total_bytes_sent >= len(file_bytes)
        self._reset_bulk_transfer_state()
        return msg

    @public
    def removeUserGrip(self, grip_name_index: GripNameIndex) -> UserGripResMsg:
        self._reset_bulk_transfer_state()
        self._file_bytes = file_bytes = BulkBytes(b'\x00' * 16)
        self._send(RemoveUserGripCmdMsg(grip_name_index=grip_name_index))
        msg1, msg2 = self._performUserGripErasing()
        msg: UserGripResMsg = self._get_message(UserGripResMsg)
        assert msg.update_status == UpdateStatus.TransferComplete
        assert self._total_bytes_sent >= len(file_bytes)
        self._reset_bulk_transfer_state()
        return msg

    @public
    def resetUserGrips(self) -> None:
        for grip_name_index, grip_path in zip(list(GripNameIndex), list(UserGripID)):
            self.sendUserGrip(grip_name_index, grip_path)

    @public
    def getGripName(self, grip_name_index: GripNameIndex) -> GripName:
        '''Get user grip name'''
        self._send(ControlMsg(msg_id=GripNameMsg.msg_id + grip_name_index, cmd_type=CommandCode.RTR, dev_id=NetDevice.HAND))
        msg: GripNameMsg = self._get_message(GripNameMsg)
        msgs: List[GripNameMsg] = [msg]
        while len(msgs) < msg.msg_total:
            next_msg: GripNameMsg = self._get_message(GripNameMsg)
            assert next_msg.msg_total == msg.msg_total
            assert next_msg.msg_num   <= msg.msg_total
            msgs.append(next_msg)
        msgs.sort(key=(lambda x: x.msg_num))
        for i, msg in enumerate(msgs):
            assert msg.msg_num == i + 1
        return GripName(''.join([msg.chars for msg in msgs]))

    @public
    def getCurrentGrip(self) -> CurrentGrip:
        '''Get the current grip config'''
        r = self._send_recv_RTR(CurrentGripMsg.msg_id)
        if r.data_len == 1:
            r: CurrentGripGripIdMsg
            return CurrentGrip(r.grip_id)
        if r.data_len == 2:
            r: CurrentGripTableMsg
            return CurrentGrip(r.table, r.table_index)
        raise Exception(f'''The CurrentGripMsg does not have a valid 'data_len'. It should be either '1' or '2' but it is '{r.data_len = }' instead.''')

    @public
    def setCurrentGrip(self, grip_id: CurrentGripID) -> CurrentGripGripIdMsg:
        '''Set the current grip via the Grip ID'''
        msg = self._send(CurrentGripGripIdMsg(cmd_type=Command(CommandCode.CMD), grip_id=grip_id))
        sleep(2**-4)
        assert grip_id
        return msg
