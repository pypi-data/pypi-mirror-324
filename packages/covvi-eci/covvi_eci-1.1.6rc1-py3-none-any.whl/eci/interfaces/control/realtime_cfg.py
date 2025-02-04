
from typing import Union

from eci.interfaces.utils import public
from eci.interfaces.enums import CommandCode
from eci.interfaces.primitives import RealtimeCfg, FourOctetAddress, Command
from eci.interfaces.messages import RealtimeCfgMsg, RealtimeCfg2Msg
from eci.interfaces.control.base_control_interface import BaseControlInterface


class RealtimeCfgInterface(BaseControlInterface):
    '''An interface to control Real-time update configuration.'''

    def __init__(self, host: Union[str, FourOctetAddress]):
        super().__init__(host)
        self._realtime_cfg: RealtimeCfg = RealtimeCfg()

    @public
    def setRealtimeCfg(self,
            digit_status:  bool = False, digit_posn:    bool = False, current_grip: bool = False, electrode_value: bool = False,
            input_status:  bool = False, motor_current: bool = False, digit_touch:  bool = False, digit_error:     bool = False,
            environmental: bool = False, orientation:   bool = False, motor_limits: bool = False,
        ) -> RealtimeCfg:
        orientation = True
        self._send(RealtimeCfgMsg.from_kwargs(cmd_type=Command(CommandCode.CMD), **locals()))
        self._send(RealtimeCfg2Msg.from_kwargs(cmd_type=Command(CommandCode.CMD), **locals()))
        self._realtime_cfg = RealtimeCfg(
            digit_status  = digit_status,  digit_posn    = digit_posn,    current_grip = current_grip, electrode_value = electrode_value,
            input_status  = input_status,  motor_current = motor_current, digit_touch  = digit_touch,  digit_error     = digit_error,
            environmental = environmental, orientation   = orientation,   motor_limits = motor_limits,
        )
        return self.realtime_cfg

    @public
    def enableAllRealtimeCfg(self) -> RealtimeCfg:
        return self.setRealtimeCfg(
            digit_status  = True, digit_posn    = True, current_grip = True, electrode_value = True,
            input_status  = True, motor_current = True, digit_touch  = True, digit_error     = True,
            environmental = True, orientation   = True, motor_limits = True,
        )

    @public
    def disableAllRealtimeCfg(self) -> RealtimeCfg:
        return self.setRealtimeCfg()

    @property
    def realtime_cfg(self) -> RealtimeCfg:
        return self._realtime_cfg
