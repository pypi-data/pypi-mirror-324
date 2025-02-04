
from typing import Callable, Union, Dict, Any
from threading import Thread
from queue import Queue, Empty
from socket import timeout

import inspect
from logging import debug
from dataclasses import dataclass

from eci.interfaces.utils import public
from eci.interfaces.base_interface import BaseInterface
from eci.primitives import FourOctetAddress
from eci.interfaces.messages import (
    RealtimeMsg, DigitStatusAllMsg, DigitPosnAllMsg, CurrentGripMsg, ElectrodeValueMsg, InputStatusMsg,
    MotorCurrentAllMsg, DigitTouchAllMsg, DigitErrorMsg, EnvironmentalMsg, OrientationMsg, MotorLimitsMsg,
    to_msg_cls,
)
from eci.interfaces.sockets import RealtimeSocket

################################################################################################################################

REALTIME_QUEUE_TIMEOUT = 0.2
REALTIME_THREAD_CALLBACK_JOIN_TIMEOUT = 3

################################################################################################################################

def do_nothing(b: RealtimeMsg):
    ...

def _check_callback(callback: Callable[[RealtimeMsg], Any], correct_type: type):
    debug(f'Checking callback function signiture: {callback.__name__} {correct_type}')
    assert callable(callback)
    # try:
    #     assert inspect.isfunction(callback)
    #     sig_params = inspect.signature(callback).parameters
    #     assert len(sig_params) == 1
    #     [callback_param] = sig_params.values()
    #     callback_annotation = str(callback_param.annotation)
    #     assert callback_annotation in {str(correct_type), str(ControlMsg)}
    # except AssertionError:
    #     raise Exception(f'''The callback parameter needs to be a function with one argument (the bytes).
    #                     The argument must be of type: {correct_type.__name__}.''')

################################################################################################################################

ALL_REALTIME_MSG_CLASSES = set((
    DigitStatusAllMsg, DigitPosnAllMsg, CurrentGripMsg, ElectrodeValueMsg, InputStatusMsg,
    MotorCurrentAllMsg, DigitTouchAllMsg, DigitErrorMsg, EnvironmentalMsg, OrientationMsg, MotorLimitsMsg,
))

@dataclass
class RealtimeInterface(BaseInterface):
    '''An interface for retrieving and processing realtime messages.'''

    n_realtime_packets: int            = 0
    orientation_msg:    OrientationMsg = None

    def __init__(self, local_host: Union[FourOctetAddress, str], local_port: int):
        debug('Initializing the realtime interface.')
        BaseInterface.__init__(self)
        self.local_host, self.local_port = local_host, local_port
        self._callback_dict: Dict[RealtimeMsg, Callable[[RealtimeMsg], Any]] = {msg_cls: do_nothing for msg_cls in ALL_REALTIME_MSG_CLASSES}
        self._realtime_packet_queue = Queue()
        self._realtime_data_thread_recv     = Thread(target=self._realtime_data_loop_recv)
        self._realtime_data_thread_callback = Thread(target=self._realtime_data_loop_callback)
        debug('Initialized the realtime interface.')

    def __enter__(self):
        debug('Starting the realtime interface.')
        BaseInterface.__enter__(self)
        self._realtime_data_thread_recv.start()
        self._realtime_data_thread_callback.start()
        debug('Started the realtime interface.')
        return self

    def __exit__(self, *args):
        debug('Closing the realtime interface.')
        self._is_running = False
        debug('Waiting for the realtime_recv thread to finish')
        self._realtime_data_thread_recv.join()
        assert not self._realtime_data_thread_recv.is_alive()
        debug('Waiting for the realtime_callback thread to finish')
        self._realtime_data_thread_callback.join(timeout=REALTIME_THREAD_CALLBACK_JOIN_TIMEOUT)
        assert not self._realtime_data_thread_callback.is_alive()
        BaseInterface.__exit__(self)
        debug('Closed the realtime interface.')

    ################################################################

    def _realtime_data_loop_recv(self):
        debug('Starting the Covvi Interface realtime socket thread')
        with RealtimeSocket(host=self.local_host, port=self.local_port) as sock:
            debug('Receiving realtime messages...')
            while self.is_running:
                try:
                    r = sock.recv()
                    self.n_realtime_packets = self.n_realtime_packets + 1
                    self._realtime_packet_queue.put(r)

                except (TimeoutError, timeout):
                    ...

        debug('Covvi Interface realtime socket thread has finished')

    def _realtime_data_loop_callback(self):
        debug('Starting the Covvi Interface realtime callback thread')
        debug('Processing realtime messages...')
        while self.is_running:
            try:
                msg: RealtimeMsg = self._realtime_packet_queue.get(timeout=REALTIME_QUEUE_TIMEOUT)
                msg_cls  = type(msg)
                callback = self._callback_dict.get(msg_cls, do_nothing)
                if msg_cls is OrientationMsg:
                    self.orientation_msg = msg
                callback(msg)

            except Empty:
                ...

        debug('Covvi Interface realtime callback thread has finished')

    ################################################################

    @property
    def callbackDigitStatusAll(self) -> Callable[[DigitStatusAllMsg], Any]:
        return self._callback_dict.get(DigitStatusAllMsg, do_nothing)

    @callbackDigitStatusAll.setter
    def callbackDigitStatusAll(self, callback: Callable[[DigitStatusAllMsg], Any]):
        debug('Setting the realtime callback for DigitStatusAllMsg')
        _check_callback(callback, DigitStatusAllMsg)
        self._callback_dict[DigitStatusAllMsg] = callback

    ################################

    @property
    def callbackDigitPosnAll(self) -> Callable[[DigitPosnAllMsg], Any]:
        return self._callback_dict.get(DigitPosnAllMsg, do_nothing)

    @callbackDigitPosnAll.setter
    def callbackDigitPosnAll(self, callback: Callable[[DigitPosnAllMsg], Any]):
        debug('Setting the realtime callback for DigitPosnMsg')
        _check_callback(callback, DigitPosnAllMsg)
        self._callback_dict[DigitPosnAllMsg] = callback

    ################################

    @property
    def callbackCurrentGrip(self) -> Callable[[CurrentGripMsg], Any]:
        return self._callback_dict.get(CurrentGripMsg, do_nothing)

    @callbackCurrentGrip.setter
    def callbackCurrentGrip(self, callback: Callable[[CurrentGripMsg], Any]):
        debug('Setting the realtime callback for CurrentGripMsg')
        _check_callback(callback, CurrentGripMsg)
        self._callback_dict[CurrentGripMsg] = callback

    ################################

    @property
    def callbackElectrodeValue(self) -> Callable[[ElectrodeValueMsg], Any]:
        return self._callback_dict.get(ElectrodeValueMsg, do_nothing)
        # return self._callback_dict.get(caElectrodeValue_a,
        #     self._callback_dict.get(caElectrodeValue_b, do_nothing)
        # )

    @callbackElectrodeValue.setter
    def callbackElectrodeValue(self, callback: Callable[[ElectrodeValueMsg], Any]):
        debug('Setting the realtime callback for ElectrodeValueMsg')
        _check_callback(callback, ElectrodeValueMsg)
        self._callback_dict[ElectrodeValueMsg] = callback
        # self._callback_dict[caElectrodeValue_a] = callback
        # self._callback_dict[caElectrodeValue_b] = callback

    ################################

    @property
    def callbackInputStatus(self) -> Callable[[InputStatusMsg], Any]:
        return self._callback_dict.get(InputStatusMsg, do_nothing)

    @callbackInputStatus.setter
    def callbackInputStatus(self, callback: Callable[[InputStatusMsg], Any]):
        debug('Setting the realtime callback for InputStatusMsg')
        _check_callback(callback, InputStatusMsg)
        self._callback_dict[InputStatusMsg] = callback

    ################################

    @property
    def callbackMotorCurrentAll(self) -> Callable[[MotorCurrentAllMsg], Any]:
        return self._callback_dict.get(MotorCurrentAllMsg, do_nothing)

    @callbackMotorCurrentAll.setter
    def callbackMotorCurrentAll(self, callback: Callable[[MotorCurrentAllMsg], Any]):
        debug('Setting the realtime callback for MotorCurrentMsg')
        _check_callback(callback, MotorCurrentAllMsg)
        self._callback_dict[MotorCurrentAllMsg] = callback

    ################################

    @property
    def callbackDigitTouchAll(self) -> Callable[[DigitTouchAllMsg], Any]:
        return self._callback_dict.get(DigitTouchAllMsg, do_nothing)

    @callbackDigitTouchAll.setter
    def callbackDigitTouchAll(self, callback: Callable[[DigitTouchAllMsg], Any]):
        debug('Setting the realtime callback for DigitTouchMsg')
        _check_callback(callback, DigitTouchAllMsg)
        self._callback_dict[DigitTouchAllMsg] = callback

    ################################

    @property
    def callbackDigitError(self) -> Callable[[DigitErrorMsg], Any]:
        return self._callback_dict.get(DigitErrorMsg, do_nothing)

    @callbackDigitError.setter
    def callbackDigitError(self, callback: Callable[[DigitErrorMsg], Any]):
        debug('Setting the realtime callback for DigitErrorMsg')
        _check_callback(callback, DigitErrorMsg)
        self._callback_dict[DigitErrorMsg] = callback

    ################################

    @property
    def callbackEnvironmental(self) -> Callable[[EnvironmentalMsg], Any]:
        return self._callback_dict.get(EnvironmentalMsg, do_nothing)

    @callbackEnvironmental.setter
    def callbackEnvironmental(self, callback: Callable[[EnvironmentalMsg], Any]):
        debug('Setting the realtime callback for EnvironmentalMsg')
        _check_callback(callback, EnvironmentalMsg)
        self._callback_dict[EnvironmentalMsg] = callback

    ################################

    @property
    def callbackOrientation(self) -> Callable[[OrientationMsg], Any]:
        return self._callback_dict.get(OrientationMsg, do_nothing)

    @callbackOrientation.setter
    def callbackOrientation(self, callback: Callable[[OrientationMsg], Any]):
        debug('Setting the realtime callback for OrientationMsg')
        _check_callback(callback, OrientationMsg)
        self._callback_dict[OrientationMsg] = callback

    ################################

    @property
    def callbackMotorLimits(self) -> Callable[[MotorLimitsMsg], Any]:
        return self._callback_dict.get(MotorLimitsMsg, do_nothing)

    @callbackMotorLimits.setter
    def callbackMotorLimits(self, callback: Callable[[MotorLimitsMsg], Any]):
        debug('Setting the realtime callback for MotorLimitsMsg')
        _check_callback(callback, MotorLimitsMsg)
        self._callback_dict[MotorLimitsMsg] = callback

    ################################

    @public
    def resetRealtimeCfg(self):
        self.n_realtime_packets = 0
        self.callbackDigitStatusAll  = do_nothing
        self.callbackDigitPosnAll    = do_nothing
        self.callbackCurrentGrip     = do_nothing
        self.callbackElectrodeValue  = do_nothing
        self.callbackInputStatus     = do_nothing
        self.callbackMotorCurrentAll = do_nothing
        self.callbackDigitTouchAll   = do_nothing
        self.callbackDigitError      = do_nothing
        self.callbackEnvironmental   = do_nothing
        self.callbackOrientation     = do_nothing
        self.callbackMotorLimits     = do_nothing
