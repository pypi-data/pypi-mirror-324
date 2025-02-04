
from sys import version_info as vi
from typing import Callable, Iterator


VERSION      = (vi.major, vi.minor)
VERSION_3_8  = (3,  8)
VERSION_3_9  = (3,  9)
VERSION_3_10 = (3, 10)
VERSION_3_11 = (3, 11)
VERSION_3_12 = (3, 12)
VERSION_3_13 = (3, 13)


def _iter_subclasses(cls, predicate: Callable[[type], bool], visited: set = None) -> Iterator[type]:
    visited = set() if visited is None else visited
    if cls not in visited:
        visited.add(cls)
        if predicate(cls):
            yield cls
        for child_cls in cls.__subclasses__():
            yield from _iter_subclasses(child_cls, predicate, visited)


def is_leaf_class(cls) -> bool:
    return len(cls.__subclasses__()) == 0


def is_branch_class(cls) -> bool:
    return len(cls.__subclasses__()) != 0


def branch_classes(cls) -> Iterator[type]:
    yield from _iter_subclasses(cls, lambda c: len(c.__subclasses__()) != 0)


def leaf_classes(cls) -> Iterator[type]:
    yield from _iter_subclasses(cls, lambda c: len(c.__subclasses__()) == 0)


def all_descendent_classes(cls) -> Iterator[type]:
    yield from _iter_subclasses(cls, lambda c: True)


BASE_STRING = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def to_base(number: int, base: int) -> str:
    assert base > 0
    assert base <= len(BASE_STRING)
    sign = '' if number >= 0 else '-'
    number = abs(number)
    if number == 0:
        return '0'
    result = ''
    while number:
        result += BASE_STRING[number % base]
        number //= base
    return f'{sign}{result[::-1]}'
