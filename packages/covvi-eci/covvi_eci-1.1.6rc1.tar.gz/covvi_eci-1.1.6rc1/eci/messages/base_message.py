
import re
import json
from typing import Iterator, Tuple, Any, List
from dataclasses import dataclass, fields


VAR_REGEX        = '{([a-zA-Z0-9_]*):0([0-9]+)b}'
BINARY_REGEX     = '([0-1]{1,8})'
WHITESPACE_REGEX = '[\n ]*'
UNPACK_REGEX     = re.compile('|'.join([VAR_REGEX, BINARY_REGEX, WHITESPACE_REGEX]))


def n_bit_mask(n: int):
    return ((1 << n) - 1)


def _unpack(format_str: str, x: bytes) -> Iterator[int]:
    bitstr = ''.join([f'{i:08b}' for i in x])
    p = 0
    for l in re.finditer(UNPACK_REGEX, format_str):
        n, j, k = l.groups()
        if p >= len(bitstr):
            break
        if j:
            j = p + int(j)
            yield int(bitstr[p:j], 2)
            p = j
        if k:
            p = p + int(l.end() - l.start())


def _n_total_bits(format_str: str) -> int:
    p = 0
    for l in re.finditer(UNPACK_REGEX, format_str):
        n, j, k = l.groups()
        if j:
            j = p + int(j)
            p = j
        if k:
            p = p + int(l.end() - l.start())
    return p


def _n_bits(format_str: str) -> Iterator[Tuple[str, int]]:
    for l in re.finditer(UNPACK_REGEX, format_str):
        name, n_arg_bits, _ = l.groups()
        if name:
            yield name, int(n_arg_bits)


def covvi_message(cls):
    return dataclass(cls, eq=True, frozen=False, unsafe_hash=True)


@covvi_message
class BaseMessage():
    FORMAT_STR = ''

    def __post_init__(self):
        kwargs_bit_lengths = {
            key: int(bit_length)
            for match in re.finditer(UNPACK_REGEX, self.FORMAT_STR)
            for key, bit_length, _ in [match.groups()]
            if bit_length
        }
        for key in kwargs_bit_lengths:
            value = getattr(self, key)
            if type(value) is int:
                setattr(self, key, value & n_bit_mask(kwargs_bit_lengths[key]))

    def __str__(self, fields: List[Tuple[str, Any]] = []) -> str:
        _fields = fields if fields else list(self.fields)
        n = max([len(k) for k, _ in _fields] + [0]) + 1
        m = max([len(type(v).__name__) for _, v in _fields] + [0])
        return '\n'.join([self.__class__.__name__] + [f'{f"{k}:":<{n}} {type(v).__name__:<{m}} = {v}' for k, v in _fields]) + '\n'

    def pack(self, *args, **kwargs) -> bytes:
        kwargs = {**{k: v for k, v in self.fields}, **kwargs}
        x = self.FORMAT_STR.replace('\n', '').format(*args, **kwargs)
        return int(x, 2).to_bytes((len(x) + 8 - 1) // 8, byteorder='big')

    def dumps(self):
        return json.dumps(self, default=lambda o: o.dict, sort_keys=True, indent=2)

    @property
    def dict(self) -> dict:
        return self.__dict__

    @property
    def fields(self) -> Iterator[Tuple[str, Any]]:
        for field in fields(self):
            yield (field.name, getattr(self, field.name))

    @classmethod
    def field_names(cls) -> Iterator[str]:
        for field in fields(cls):
            yield field.name

    @classmethod
    def field_types(cls) -> Iterator[type]:
        for field in fields(cls):
            yield field.type

    @classmethod
    def field_names_types(cls) -> Iterator[Tuple[str, type]]:
        for name, type in zip(cls.field_names(), cls.field_types()):
            yield name, type

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(**{k:kwargs[k] for k in cls.field_names() if k in kwargs})

    @classmethod
    def unpack(cls, b: bytes):
        return cls(*tuple(_unpack(cls.FORMAT_STR, b)))
