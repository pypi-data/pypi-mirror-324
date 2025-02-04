
import os
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_UDP
from logging import debug
from typing import Optional, Tuple

from eci.sockets.primitives import FourOctetAddress
from eci.sockets.messages import DiscoveryResponseMsg
from eci.sockets.discovery.discovery_socket import DiscoverySocket


DISCOVERY_RECEIVING_ADDRESS = str(FourOctetAddress(os.environ.get('DISCOVERY_RECEIVING_ADDRESS', '')))


class DiscoveryReceivingSocket(DiscoverySocket):
    '''A UDP socket for receiving discovery responses from an ECI.'''

    def __init__(self):
        debug(f'''Initializing discovery socket port={DiscoverySocket.PORT}''')
        super().__init__(host='', port=DiscoverySocket.PORT, family=AF_INET, type=SOCK_DGRAM, proto=IPPROTO_UDP)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.settimeout(DiscoverySocket.TIMEOUT)
        debug(f'''Initialized discovery socket port={DiscoverySocket.PORT}''')

    def __enter__(self):
        debug('Binding discovery receiving socket')
        super().__enter__()
        self.bind((DISCOVERY_RECEIVING_ADDRESS, DiscoverySocket.PORT))
        debug('Bound discovery receiving socket')
        return self

    def recvfrom_disco_packet(self) -> Tuple[Optional[DiscoveryResponseMsg], Tuple[str, int]]:
        debug(f'recvfrom_disco_packet on port {DiscoverySocket.PORT}')
        data, addr = self.recvfrom(DiscoverySocket.RECV_LENGTH)
        try:
            msg = DiscoveryResponseMsg.unpack(data)
            debug(f'Received {msg} from {addr}')
            return msg, addr
        except TypeError:
            return None, addr
