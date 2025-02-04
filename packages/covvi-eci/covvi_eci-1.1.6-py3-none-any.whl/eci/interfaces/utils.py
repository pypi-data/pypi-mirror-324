
from typing import Callable


def public(func: Callable) -> Callable:
    setattr(func, 'public', True)
    return func
