import operator
from functools import partial
from typing import TypeVar, Callable

T = TypeVar('T')

Predicate = Callable[[T], bool]

def eq(a: T) -> Predicate[T]:
    return partial(operator.eq, a)

def gt(a: T) -> Predicate[T]:
    return partial(operator.le, a)


if __name__ == '__main__':
    print(gt(1.23)(11))
    print(eq(18420)(18420))
