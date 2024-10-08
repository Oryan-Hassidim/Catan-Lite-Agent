
from typing import Generic, Iterable, Iterator, TypeVar


T = TypeVar('T')


class frozenlist(Generic[T]):
    def __init__(self, *iterable: T):
        self.__data = tuple(iterable)

    def __iter__(self) -> Iterator[T]:
        return iter(self.__data)

    def __contains__(self, item) -> bool:
        return item in self.__data

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self) -> str:
        return f"dupfrozenset({self.__data})"

    def __getitem__(self, index: int) -> T:
        return self.__data[index]
        
    def copy(self):
        return frozenlist(self.__data)
    
    def update_item(self, index: int, item: T) -> 'frozenlist[T]':
        return frozenlist(*self.__data[:index], item, *self.__data[index + 1:])
    
    def rotate(self, n: int = 1) -> 'frozenlist[T]':
        n = n % len(self.__data)
        return frozenlist(*self.__data[n:], *self.__data[:n])

    def __eq__(self, other: 'frozenlist') -> bool:
        return (isinstance(other, frozenlist)
                and self.__data == other.__data)

    def __ne__(self, other: 'frozenlist') -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.__data)
