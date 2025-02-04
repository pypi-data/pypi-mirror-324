
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class BasePrimitive():

    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return int(self).__format__(format_spec)
        else:
            return str(self)

    @property
    def dict(self) -> dict:
        return self.__dict__
