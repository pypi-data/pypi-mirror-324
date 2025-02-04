
import os
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST, IPPROTO_UDP
from logging import debug

from eci.primitives import FourOctetAddress
from eci.sockets.messages import DiscoveryRequestMsg, DiscoveryConfigMsg
from eci.sockets.discovery.discovery_socket import DiscoverySocket


DISCOVERY_SENDING_ADDRESS = str(FourOctetAddress(os.environ.get('DISCOVERY_SENDING_ADDRESS', '255.255.255.255')))


class CannotAssignAddress(Exception): ...


class DiscoverySendingSocket(DiscoverySocket):
    '''A UDP socket for sending discovery requests and configuration messages.'''

    def __init__(self, host: str = ''):
        debug(f'''Initializing discovery sending socket host='{host}' port={DiscoverySocket.PORT}''')
        super().__init__(host=host, port=DiscoverySocket.PORT, family=AF_INET, type=SOCK_DGRAM, proto=IPPROTO_UDP)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.settimeout(DiscoverySocket.TIMEOUT)
        debug(f'''Initialized discovery sending socket host='{host}' port={DiscoverySocket.PORT}''')

    def __enter__(self):
        debug('Binding discovery sending socket')
        super().__enter__()
        try:
            self.bind((self.host, self.port))
        except OSError as e:
            if e.errno == 99: # Cannot assign requested address
                raise CannotAssignAddress(f'Could not bind to {self.host}:{self.port}. Check that you have a network interface with this IP address.')
            else:
                raise e
        debug('Bound discovery sending socket')
        return self

    def send_request(self, sending_address: str = DISCOVERY_SENDING_ADDRESS) -> int:
        msg = DiscoveryRequestMsg()
        debug(f'{msg} has been sent to {sending_address} on port {DiscoverySocket.PORT}')
        return self.sendto(msg.pack(), (sending_address, DiscoverySocket.PORT))

    def send_config(self, msg: DiscoveryConfigMsg, addr: str) -> int:
        debug(f'{msg} has been sent to {addr} on port {DiscoverySocket.PORT}')
        return self.sendto(msg.pack(), (addr, DiscoverySocket.PORT))
