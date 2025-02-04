
from logging import debug
from typing import Union

from eci.interfaces.control.basic                  import BasicControlInterface
from eci.interfaces.control.realtime_cfg           import RealtimeCfgInterface
from eci.interfaces.control.digit                  import DigitInterface
from eci.interfaces.control.digit_config           import DigitConfigInterface
from eci.interfaces.control.direct_control         import DirectControlInterface
from eci.interfaces.control.system_status          import SystemStatusInterface
from eci.interfaces.control.user_grip              import UserGripInterface
from eci.interfaces.control.base_control_interface import BaseControlInterface
from eci.interfaces.primitives                     import FourOctetAddress


class ControlInterface(
        BasicControlInterface,
        RealtimeCfgInterface,
        DigitInterface,
        DigitConfigInterface,
        DirectControlInterface,
        SystemStatusInterface,
        UserGripInterface,
        BaseControlInterface,
    ):
    '''An interface to combine all functionality from the various control interfaces into a single one.'''

    def __init__(self, host: Union[FourOctetAddress, str]):
        debug('Initializing the Control Interface')
        super().__init__(host)
        debug('Initialized the Control Interface')

    def __enter__(self):
        debug('Starting the Control Interface')
        super().__enter__()
        debug('Started the Control Interface')
        return self

    def __exit__(self, *args):
        debug('Closing the Control Interface')
        super().__exit__()
        debug('Closed the Control Interface')
