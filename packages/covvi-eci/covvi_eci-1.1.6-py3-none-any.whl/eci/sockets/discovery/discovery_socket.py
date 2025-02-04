
from eci.sockets.base_socket import BaseSocket


class DiscoverySocket(BaseSocket):
    PORT:        int   = 8998
    TIMEOUT:     float = 0.05
    RECV_LENGTH: int   = 256
