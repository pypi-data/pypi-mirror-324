
from typing      import overload
from dataclasses import dataclass

from eci.primitives.enums          import ProductString, ProductID
from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class Product(BasePrimitive):
    value: ProductString = ProductString.NONE
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, integer: int): ...
    @overload
    def __init__(self, product_id: ProductID): ...
    @overload
    def __init__(self, product_string: ProductString): ...
    def __init__(self, value = ProductString.NONE):
        if isinstance(value, str):
            self.value = ProductString(value)
            return
        if isinstance(value, int):
            self.value = ProductID(value).str()
            return
        if isinstance(value, ProductID):
            self.value = value.str()
            return
        if isinstance(value, ProductString):
            self.value = value
            return
        if isinstance(value, Product):
            self.value = value.value
            return

    def __str__(self) -> str:
        return str(self.value)
    def __int__(self) -> int:
        return int(self.value.int())
    def str(self) -> ProductString:
        return self.value
    def int(self) -> ProductID:
        return self.value.int()


Product.__doc__ = f'''This is a class to represent a Product. Its possible values are:
{', '.join([product_id.name for product_id in ProductID])}.'''
