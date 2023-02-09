import itertools
from functools import partial, reduce
from inspect import signature
from typing import TypeVar, Callable


def Y(f):
    return (lambda x: f(x(x)))(lambda x: f(x(x)))


def Z(f):
    return (lambda x: f(lambda *y: x(x)(*y)))(lambda x: f(lambda *y: x(x)(*y)))


def fix(f):
    return f(lambda x: fix(f)(x))


def curried(f):
    return f if len(signature(f).parameters) == 1 else lambda x: curried(partial(f, x))


T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')


def identity(x: T) -> T:
    return x


def compose(after: Callable[[T2], T3], before: Callable[[T1], T2]) -> Callable[[T1], T3]:
    return lambda x: after(before(x))


def mapply(f: Callable[[T], T], n: int) -> Callable[[T], T]:
    return reduce(compose, itertools.repeat(f, n), identity)


if __name__ == '__main__':
    fib_40 = Z(lambda f: curried(lambda a0, a1, n: a0 if n <= 0 else f(a1)(a0+a1)(n-1)))(0)(1)(40)
    print(fib_40)

    from os.path import dirname

    grandpa = mapply(dirname, 2)

    print(grandpa(r'\hoge\huga\foo\bar.txt'))
