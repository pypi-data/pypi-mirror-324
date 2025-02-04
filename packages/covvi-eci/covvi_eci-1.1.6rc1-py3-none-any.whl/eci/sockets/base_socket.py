
from socket import socket, AF_INET, SOCK_STREAM, SocketKind, IPPROTO_UDP
from typing import Iterator, List

from eci.sockets.messages import (
    UserGripResMsg, UploadDownLoadMsg, BaseControlMsg, ControlMsg, BulkRequestMsg, BulkResponseMsg,
    FirmwarePicMsg, EciFirmwarePicMsg, HandFirmwarePicMsg,
    to_msg_cls,
)
from eci.sockets.enums import UID_DELIMITER, CommandCode, BulkDataType


class BaseSocket(socket):
    def __init__(self, host: str, port: int, family: int = AF_INET, type: SocketKind = SOCK_STREAM, proto: int = IPPROTO_UDP):
        self.host, self.port = host, port
        super().__init__(family=family, type=type, proto=proto)

    def __process_bytes(self, b: bytes) -> Iterator[ControlMsg]:
        for msg in b.split(UID_DELIMITER)[1:]:
            msg = UID_DELIMITER + msg
            
            cls = {
                CommandCode.BLK_RTR: BulkRequestMsg,
                CommandCode.BLK:     BulkResponseMsg,
            }.get(BaseControlMsg.unpack(msg).cmd_type.int())
            
            if not cls:
                msg_id = ControlMsg.unpack(msg).msg_id
                cls = to_msg_cls(msg_id)
                
                if cls is UploadDownLoadMsg:
                    data_type = UploadDownLoadMsg.unpack(msg).data_type
                    cls = {
                        BulkDataType.GRIP: UserGripResMsg,
                    }[data_type]

                if issubclass(cls, FirmwarePicMsg):
                    dev_id = FirmwarePicMsg.unpack(msg).dev_id
                    cls = {
                        EciFirmwarePicMsg.dev_id:  EciFirmwarePicMsg,
                        HandFirmwarePicMsg.dev_id: HandFirmwarePicMsg,
                    }[dev_id]
            
            covvi_msg = cls.unpack(msg)
            yield covvi_msg

    def _process_bytes(self, b: bytes) -> List[ControlMsg]:
        return list(self.__process_bytes(b))
