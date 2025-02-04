
from datetime import datetime
from typing   import Iterator, Optional, Tuple, Set
from logging  import debug
from time     import sleep
from socket   import timeout

from eci.interfaces.primitives     import FourOctetAddress
from eci.interfaces.base_interface import BaseInterface
from eci.interfaces.messages       import DiscoveryResponseMsg, DiscoveryConfigMsg
from eci.interfaces.sockets        import DiscoverySendingSocket, DiscoveryReceivingSocket, DISCOVERY_SENDING_ADDRESS


IGNORE_REQUEST_SOURCE_ADDRESSES: Set[str] = set(['0.0.0.0'])
TIME_FOR_SINGLE_DISCOVERY:       float    = 5.0


class DiscoveryInterface(BaseInterface):
    '''An interface to request and configure discovery information about the ECI.'''

    def __init__(self, *hosts: Tuple[str, ...]):
        debug(f'Initializing discovery interface on hosts="{hosts}"')
        super().__init__()
        self.hosts = hosts
        self._sending_sockets  = [DiscoverySendingSocket(host) for host in hosts] if len(hosts) else [DiscoverySendingSocket()]
        self._receiving_socket = DiscoveryReceivingSocket()

    def __enter__(self):
        super().__enter__()
        self._receiving_socket.__enter__()
        for socket in self._sending_sockets:
            socket.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        for socket in self._sending_sockets:
            socket.__exit__()
        self._receiving_socket.__exit__()
        super().__exit__(*args, **kwargs)

    ################################################################

    def send_request(self, sending_address: str = DISCOVERY_SENDING_ADDRESS) -> int:
        return [socket.send_request(sending_address=sending_address) for socket in self._sending_sockets]

    def send_config(self, msg: DiscoveryConfigMsg, addr: str) -> int:
        for socket in self._sending_sockets:
            r = socket.send_config(msg, str(FourOctetAddress(addr)))
        return r

    def recvfrom_disco_packet(self) -> Tuple[Optional[DiscoveryResponseMsg], Tuple[str, int]]:
        return self._receiving_socket.recvfrom_disco_packet()

    ################################################################

    def get_eci_list(self) -> Iterator[Tuple[Optional[DiscoveryResponseMsg], Tuple[str, int]]]:
        while True:
            sleep(2**-4)
            try:
                msg, addr = msg, (host, port) = self.recvfrom_disco_packet()
                request_source_address = str(msg.request_source_address)
                if host not in self.hosts and request_source_address not in IGNORE_REQUEST_SOURCE_ADDRESSES:
                    if request_source_address in self.hosts or len(self.hosts) == 0:
                        yield msg, addr
            except (TimeoutError, timeout):
                break

    def forever_get_eci_list(self):
        while True:
            self.send_request()
            yield from self.get_eci_list()


def get_discovery_from_serial(*ip_addresses: Tuple[str], serial_number: int = 0) -> DiscoveryResponseMsg:
    with DiscoveryInterface(*ip_addresses) as interface:
        for msg, addr in interface.forever_get_eci_list():
            if msg.device_serial_number == serial_number:
                return msg


def is_existing_connection(ip_address: str) -> bool:
    with DiscoveryInterface() as interface:
        start = datetime.now()

        while True:
            interface.send_request(sending_address=str(ip_address))

            for msg, (ip, port) in interface.get_eci_list():
                if str(ip) == str(ip_address):
                    return msg.client_connected

            end = datetime.now()
            elapsed_time = (end - start).total_seconds()

            if elapsed_time >= TIME_FOR_SINGLE_DISCOVERY:
                break

    return False
