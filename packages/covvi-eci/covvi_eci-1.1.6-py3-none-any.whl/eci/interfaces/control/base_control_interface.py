
from dataclasses import dataclass
from logging     import debug, warning
from time        import sleep
from typing      import Union, List, Dict, Callable, Optional
from threading   import Thread
from queue       import Queue
from socket      import timeout

from eci.interfaces.primitives     import Command, FourOctetAddress
from eci.interfaces.enums          import MessageID, CommandCode
from eci.interfaces.messages       import BaseMessage, ControlMsg, to_msg_cls
from eci.interfaces.sockets        import ControlSocket
from eci.interfaces.base_interface import BaseInterface
from eci.interfaces.discovery      import is_existing_connection
from eci                           import all_descendent_classes


N_CONNETION_ATTEMPTS: int = 3


class ControlTimeoutError(Exception): ...
class ExistingConnectionError(Exception): ...


@dataclass
class BaseControlInterface(BaseInterface):
    '''An interface to control various functionality of the hand.'''

    n_control_packets: int = 0

    def __init__(self, host: Union[str, FourOctetAddress]):
        debug('Initializing the base control interface.')
        super().__init__()

        self.host:        FourOctetAddress = FourOctetAddress(host)
        self._ctl_socket: ControlSocket    = None

        self._exception:                     Exception = None
        self._existing_connection_exception: Exception = None

        self._control_data_thread_recv:   Thread = Thread(target=self._control_data_loop_recv, args=(self.host,))
        self._existing_connection_thread: Thread = Thread(target=self._discover_existing_connection, args=(self.host,))

        self._message_queues: Dict[type, Queue] = {cls: Queue() for cls in all_descendent_classes(BaseMessage)}
        self._message_dict:   Dict[type, Callable[[ControlMsg], None]] = {}

        debug('Initialized the base control interface.')

    def __enter__(self):
        debug('Starting the base control interface.')
        super().__enter__()
        self._existing_connection_thread.start()
        self._control_data_thread_recv.start()

        while (not self._ctl_socket) and (not (self._exception or self._existing_connection_exception)):
            sleep(2**-4)

        if self._existing_connection_exception:
            raise self._existing_connection_exception

        if self._exception:
            raise self._exception

        debug('Started the base control interface.')
        return self

    def __exit__(self, *args):
        debug('Closing the base control interface.')
        self._is_running = False
        debug('Waiting for the control_recv thread to finish')
        self._control_data_thread_recv.join()
        assert not self._control_data_thread_recv.is_alive()
        super().__exit__()
        debug('Closed the base control interface.')

    ################################################################

    def _process_message(self, msg: ControlMsg) -> None:
        self._message_queues[type(msg)].put(msg)

    def _get_message(self, cls: type) -> BaseMessage:
        return self._message_queues[cls].get()

    def _get_messages(self, cls: type) -> List[BaseMessage]:
        msgs = []
        while not self._message_queues[cls].empty():
            msgs.append(self._message_queues[cls].get())
        return msgs

    def _discover_existing_connection(self, host: Union[FourOctetAddress, str]) -> None:
        sleep(2)
        if is_existing_connection(host):
            self._existing_connection_exception = ExistingConnectionError(f'Failed to connect to {self.host} on port {ControlSocket.PORT} due to existing connection.')

    def _init_control_socket(self, host: Union[FourOctetAddress, str]) -> Optional[Exception]:
        for i in range(N_CONNETION_ATTEMPTS):
            try:
                _ctl_socket = ControlSocket(host=host).__enter__()

            except TimeoutError:
                _ctl_socket = None
                if self._existing_connection_exception:
                    _exception = self._existing_connection_exception
                    break
                else:
                    timeout_message = f'Failed to connect to {self.host}:{ControlSocket.PORT} due to timeout, attempt {i+1}/{N_CONNETION_ATTEMPTS}.'
                    _exception = ControlTimeoutError(timeout_message)
                    warning(timeout_message)

            else:
                _exception = None
                break

        self._ctl_socket, self._exception = _ctl_socket, _exception
        return _exception

    def _control_data_loop_recv(self, host: Union[FourOctetAddress, str]) -> None:
        debug('Starting the Covvi Interface control socket thread')

        if self._init_control_socket(host):
            return

        debug('Receiving control messages...')
        while self.is_running:
            try:
                for r in self._ctl_socket.recv():
                    self.n_control_packets = self.n_control_packets + 1
                    self._message_dict.get(type(r), self._process_message)(r)

            except (TimeoutError, timeout):
                ...

        self._ctl_socket.__exit__()

        debug('Covvi Interface control socket thread has finished')

    ################################################################

    def _send_recv_RTR(self, msg_id: MessageID) -> ControlMsg:
        debug(f'Request and Retrieve values: msg_id = {msg_id:05X} {msg_id.value}')
        cls = to_msg_cls(msg_id)
        msg = cls(msg_id=msg_id, cmd_type=Command(CommandCode.RTR), dev_id=cls.dev_id)
        self._ctl_socket.send(msg)
        return self._get_message(type(msg))

    def _send(self, msg: ControlMsg) -> ControlMsg:
        return self._ctl_socket.send(msg)
