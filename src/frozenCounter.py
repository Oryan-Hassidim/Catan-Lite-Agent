
from typing import Generic, Iterable, Iterator, TypeVar

from helpers import fst


T = TypeVar('T')


class frozenCounter(Generic[T]):
    def __init__(self, elements: dict[T, int] = {}):
        self._data: dict[T, int] = {item: value
                                    for item, value in sorted(elements.items(), key=fst) # type: ignore
                                    if value != 0}
        self._hash = hash(tuple(self._data.items()))

    def items(self) -> Iterable[tuple[T, int]]:
        return self._data.items()

    def __getitem__(self, key: T) -> int:
        return self._data.get(key, 0)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __eq__(self, other: 'frozenCounter') -> bool:
        return self._data == other._data

    def __ne__(self, other: 'frozenCounter') -> bool:
        return self._data != other._data

    def __hash__(self) -> int:
        return self._hash

    def __add__(self, other: 'frozenCounter') -> 'frozenCounter':
        return frozenCounter({item: self[item] + other[item]
                              for item in self._data})

    def __sub__(self, other: 'frozenCounter') -> 'frozenCounter':
        return frozenCounter({item: self[item] - other[item]
                              for item in self._data})

    def __contains__(self, item: 'frozenCounter') -> bool:
        return all(self[item] >= item[item] for item in item)
