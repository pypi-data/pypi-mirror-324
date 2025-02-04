
from typing import Tuple, Any


def fStrBits(*strings: Tuple[str, ...], k: int = 1) -> str:
    if len(strings) == 1:
        string, = strings
        return ''.join(f'{{{s}:0{k}b}}' for s in string.split())
    if len(strings) > 1:
        *strings, str1, str2 = strings
        return fStrBits(*strings, ' '.join([
            f'{_str1}_{_str2}'
            for _str1 in str1.split()
            for _str2 in str2.split()
        ]), k=k)
    return ''


def tobool(value: Any) -> bool:
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(int(value))
