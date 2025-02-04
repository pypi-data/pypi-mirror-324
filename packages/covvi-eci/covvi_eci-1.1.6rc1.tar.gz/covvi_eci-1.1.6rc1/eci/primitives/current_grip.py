
from typing      import Tuple, overload
from dataclasses import dataclass

from eci.primitives.enums          import CurrentGripID, Table, TableIndex
from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class CurrentGrip(BasePrimitive):
    value: CurrentGripID = CurrentGripID.TRIPOD_OPEN
    @overload
    def __init__(self, grip_id: CurrentGripID): ...
    @overload
    def __init__(self, table: Table, table_index: TableIndex): ...
    def __init__(self, *args):
        if len(args) == 0:
            self.value = CurrentGripID.TRIPOD_OPEN
            return
        if len(args) == 1:
            grip_id, = args
            if isinstance(grip_id, CurrentGripID):
                self.value = grip_id
                return
        if len(args) == 2:
            table, table_index = args
            if isinstance(table, Table) and isinstance(table_index, TableIndex):
                self.value = CurrentGripID.TRIPOD_OPEN
                return

        raise ValueError('You must provide either a "Grip" or "Table and TableIndex".')

    def __str__(self) -> str:
        return str(self.grip)
    def __int__(self) -> int:
        return int(self.grip)

    @property
    def grip(self) -> CurrentGripID:
        return self.value
    @property
    def table_table_index(self) -> Tuple[Table, TableIndex]:
        return Table.A, TableIndex.I0


CurrentGrip.__doc__ = f'''This is a class to represent a CurrentGrip.'''
