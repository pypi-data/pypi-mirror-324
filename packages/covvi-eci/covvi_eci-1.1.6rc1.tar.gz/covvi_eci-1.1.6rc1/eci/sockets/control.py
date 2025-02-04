
from socket import SOCK_STREAM, IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from logging import debug
from typing import Union, List

from eci.sockets.primitives import FourOctetAddress
from eci.sockets.messages import ControlMsg
from eci.sockets.base_socket import BaseSocket


class ControlSocket(BaseSocket):
    '''A TCP socket for sending and receiving control messages.'''

    PORT:            int   = 4267
    CONNECT_TIMEOUT: float = 10.0
    TIMEOUT:         float = 0.2
    RECV_LENGTH:     int   = 256

    def __init__(self, host: Union[FourOctetAddress, str]):
        debug('Initializing the control socket for sending and receiving messages')
        super().__init__(host=host, port=ControlSocket.PORT, type=SOCK_STREAM, proto=IPPROTO_TCP)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.settimeout(ControlSocket.CONNECT_TIMEOUT)
        debug('Initialized the control socket')

    def __enter__(self):
        debug(f'Connecting to the control port host={self.host} port={self.port}')
        super().__enter__()
        self.connect((str(FourOctetAddress(self.host)), self.port))
        self.settimeout(ControlSocket.TIMEOUT)
        debug(f'Connected to the control port host={self.host} port={self.port}')
        return self

    def send(self, msg: ControlMsg) -> ControlMsg:
        debug(f'''Sending control message: id={id(msg)}
{msg}''')
        super().send(msg.pack())
        debug(f'Sent control message: id={id(msg)}')
        return msg

    def recv(self) -> List[ControlMsg]:
        r = self._process_bytes(super().recv(ControlSocket.RECV_LENGTH))
        for _r in r:
            debug(f'''Received control message id={id(_r)}
{_r}''')
        return r
