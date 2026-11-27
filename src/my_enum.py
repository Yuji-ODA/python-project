from enum import Enum
from typing import Optional, TypeVar, Generic


class AutoNumberEnum(Enum):
    def __new__(cls, *args):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def for_name(cls, name: str) -> Optional['AutoNumberEnum']:
        return next((x for x in cls if x.name == name), None)

_FlagCombinator = TypeVar('_FlagCombinator', bound='FlagCombinator')
class FlagCombinator(Generic[_FlagCombinator]):
    def __init__(self, index: int) -> None:
        self.__index = index

    @property
    def index(self) -> int:
        return self.__index

    def __or__(self, other: 'FlagCombinator[_FlagCombinator]') -> 'FlagCombinator[_FlagCombinator]':
        return FlagCombinator(self.__index | other.__index)

    def __and__(self, other: 'FlagCombinator[_FlagCombinator]') -> 'FlagCombinator[_FlagCombinator]':
        return FlagCombinator(self.__index & other.__index)

    __add__ = __or__

    def __sub__(self, other: 'FlagCombinator[_FlagCombinator]') -> 'FlagCombinator[_FlagCombinator]':
        return FlagCombinator(self.__index - (self.__index & other.__index))

    def __eq__(self, other: 'FlagCombinator[_FlagCombinator]') -> bool:
        return self.__index == other.__index

    def __contains__(self, other: 'FlagCombinator[_FlagCombinator]') -> bool:
        return self.__index == self.__index & other.__index

    def __iter__(self) -> str:
        return f'{self.__class__.__name__}(index={self.__index})'

class FlagCombinatorMixin(FlagCombinator[_FlagCombinator]):
    def __init__(self) -> None:
        super().__init__(1 << (self.value - 1))

    @classmethod
    def unpack(cls, flag_combinator: FlagCombinator[_FlagCombinator]) -> list[_FlagCombinator]:
        return [flag_enum for flag_enum in cls if flag_enum in flag_combinator]

class Destination(FlagCombinatorMixin['Destination'], AutoNumberEnum):
    def __init__(self, name: str):
        super().__init__()
        self._name_ = name

    NONE = '指定なし'
    NHK = 'NHK'
    FUKUI_PREF = '福井県'

if __name__ == '__main__':
    none = Destination.NONE

    destination = Destination.for_name('福井県')

    print(destination)

    def f(x: Destination) -> str:
        match x:
            case Destination.NONE:
                return 'none'
            case Destination.NHK:
                return 'nhk'
            case Destination.FUKUI_PREF:
                return 'fukui'


    print(f(Destination.NONE))
