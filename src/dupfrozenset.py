
from typing import Generic, Iterable, Iterator, TypeVar


T = TypeVar('T')


class dupfrozenset(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self.data: list[T] = list(sorted(iterable, key=hash))

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __contains__(self, item) -> bool:
        return item in self.data

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f"dupfrozenset({self.data})"

    def copy(self):
        return dupfrozenset(self.data)

    def __eq__(self, other: 'dupfrozenset') -> bool:
        return self.data == other.data

    def __ne__(self, other: 'dupfrozenset') -> bool:
        return self.data != other.data

    def __hash__(self) -> int:
        return hash(tuple(self.data))
