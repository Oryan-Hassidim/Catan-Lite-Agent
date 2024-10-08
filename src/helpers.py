
from typing import Iterable, TypeVar


T = TypeVar('T')


def fst(x: tuple[T, int]) -> T:
    return x[0]

