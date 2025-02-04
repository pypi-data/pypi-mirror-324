
from socket import SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_UDP
from logging import debug
from typing import Union

from eci.sockets.messages import ControlMsg, RealtimeMsg, to_msg_cls
from eci.sockets.base_socket import BaseSocket
from eci.sockets.primitives import FourOctetAddress


class RealtimeSocket(BaseSocket):
    '''A UDP socket for receiving real-time messages.'''

    TIMEOUT:     float = 0.2
    RECV_LENGTH: int   = 256

    def __init__(self, host: Union[FourOctetAddress, str], port: int):
        host = str(FourOctetAddress(host))
        debug(f'''Initializing realtime socket for receiving messages only host='{host}' port={port}''')
        super().__init__(host=host, port=port, type=SOCK_DGRAM, proto=IPPROTO_UDP)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.settimeout(RealtimeSocket.TIMEOUT)
        debug(f'''Initialized realtime socket host='{host}' port={port}''')

    def __enter__(self):
        debug('Binding realtime socket')
        super().__enter__()
        self.bind((self.host, self.port))
        debug('Bound realtime socket')
        return self

    def recv(self) -> RealtimeMsg:
        data, addr = self.recvfrom(RealtimeSocket.RECV_LENGTH)
        msg_id = ControlMsg.unpack(data).msg_id
        msg_cls = to_msg_cls(msg_id)
        return msg_cls.unpack(data)
