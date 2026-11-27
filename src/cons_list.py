from collections.abc import Iterable, Iterator, Sequence, Reversible
from functools import reduce
from typing import TypeVar, Optional, Callable, overload, Union

T = TypeVar('T')
U = TypeVar('U')

def expand_indices(start: int, stop: int, step: int) -> Iterator[int]:
    if step == 0:
        raise ValueError('slice step cannot be zero')
    i = start
    while (i < stop) is (0 < step):
        yield i
        i += step

def expand_strides(start: int, stop: int, step: int) -> Iterator[int]:
    if step == 0:
        raise ValueError('slice step cannot be zero')
    s = 0
    p = start
    while (p < stop) is (0 < step):
        yield p - s
        s = p
        p += step

class Cons(Sequence[T]):

    def __init__(self, value: T, tail: Optional['Cons[T]'] = None):
        self.__value = value
        self.__tail = tail
        self.__depth = 1 if tail is None else tail.__depth + 1

    @property
    def value(self) -> T:
        return self.__value

    @property
    def tail(self) -> 'Cons[T]':
        return self.__tail

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> Optional['Cons[T]']:
        def reducer(acc: Optional['Cons[T]'], t: T) -> Optional['Cons[T]']:
            return cls(t, acc)
        return reduce(reducer, reversed(iterable if isinstance(iterable, (Reversible, Sequence)) else tuple(iterable)), None)

    def __rshift__(self, value: T) -> 'Cons[T]':
        """
        末尾に値を追加する

        Params:
            value: 追加する値

        Returns:　追加したリスト
        """
        return self.fold_right(self.__class__, self.__class__(value))

    def __add__(self, other: 'Cons[T]') -> 'Cons[T]':
        """
        リストを結合する
        Args:
            other: 結合するリスト

        Returns:
            'Cons[T]': 

        Returns: 結合したリスト

        """
        return self.fold_right(self.__class__, other)

    def __len__(self) -> int:
        return self.__depth

    def sub_list(self, i: int) -> Optional['Cons[T]']:
        i = i + self.__depth if i < 0 else i
        return self if i == 0 else self.__tail and self.__tail.sub_list(i - 1)

    def reversed(self) -> 'Cons[T]':
        return self.fold_left(lambda acc, x: self.__class__(x, acc))

    def map(self, function: Callable[[T], U]) -> 'Cons[U]':
        return self.fold_right(lambda x, acc: self.__class__(function(x), acc))

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> 'Cons[T]': ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, 'Cons[T]']:
        if isinstance(index, int):
            index += self.__depth if index < 0 else 0
            if self.__depth <= index or index < 0:
                raise IndexError('list index out of range')
            return next(v for i, v in enumerate(self) if i == index)
        elif isinstance(index, slice):
            return self.__class__.from_iterable(list(self)[index])
            # return self.__class__.from_iterable(map(self.__getitem__, expand_indices(*index.indices(self.__depth))))
        else:
            raise TypeError('index must be int or slice')

    def __iter__(self) -> Iterator[T]:
        item = self
        while item is not None:
            yield item.__value
            item = item.__tail

    def fold_left(self, function: Callable[[U, T], U], initial: Optional[U] = None) -> U:
        acc = initial
        item = self
        while item is not None:
            acc = function(acc, item.__value)
            item = item.__tail
        return acc

    def fold_right(self, function: Callable[[T, U], U], initial: Optional[U] = None) -> U:
        return self.reversed().fold_left(lambda u, t: function(t, u), initial)

    def __str__(self) -> str:
        return self.fold_right(lambda x, acc: f'[{x}]->{acc}', 'Nil')


if __name__ == '__main__':
    cl = Cons.from_iterable(range(10))
    print(cl)
    print(list(cl))
    print(len(cl))
    print(cl[3])
    print(cl.map(lambda x: x*2+1))
    print(cl.reversed())
    print(cl[2:8:3])
    print(cl[5:1:-3])
    print(cl[1:5:-3])
    print(cl.sub_list(-2))

    print(Cons.from_iterable(range(10000000))[9999999])
