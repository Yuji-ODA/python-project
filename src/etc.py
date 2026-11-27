from my_enum import Enum
from typing import Optional, Generic, TypeVar

from typing_extensions import Self

T = TypeVar('T')

class FlagCombinator(Generic[T]):
    def __init__(self, index: int):
        self.__index = index

    def __or__(self, other: 'FlagCombinator[T]') -> 'FlagCombinator[T]':
        return FlagCombinator(self.__index | other.__index)

    def __and__(self, other: 'FlagCombinator[T]') -> 'FlagCombinator[T]':
        return FlagCombinator(self.__index & other.__index)

    __add__ = __or__

    def __sub__(self, other: 'FlagCombinator[T]') -> 'FlagCombinator[T]':
        return FlagCombinator(self.__index - (self.__index & other.__index))

    def __eq__(self, other: 'FlagCombinator[T]') -> bool:
        return self.__index == other.__index

    def __contains__(self, item: 'FlagCombinator[T]') -> bool:
        return item.__index == self.__index & item.__index

    def __str__(self):
        return f'{self.__class__.__name__}(index={self.__index})'


class AutoNumberEnum(Enum):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__) + 1
        return obj

    @classmethod
    def of(cls, name: str) -> Optional[Self]:
        return next((x for x in cls if x.name == name), None)

class FlagEnum(FlagCombinator[T], AutoNumberEnum):
    def __init__(self):
        super().__init__(1 << (self.value - 1))

    @classmethod
    def unpack(cls, flag_combinator: FlagCombinator[T]) -> list[T]:
        return [flag_enum for flag_enum in cls if flag_enum in flag_combinator]

    def __str__(self):
        return super(Enum, self).__str__()
