import random
import sys
import timeit
from collections.abc import Iterator
from itertools import groupby, islice, chain, pairwise
from typing import Iterable, Generator, Callable


def group_by_key(f):
    return lambda x: {k: tuple(v) for k, v in groupby(sorted(x, key=f), f)}


def flatten[T](src: Iterable[T]) -> Generator[T, None, None]:
    for elem in src:
        if isinstance(elem, Iterable) and not isinstance(elem, str):
            yield from flatten(elem)
        else:
            yield elem

def uniq[T](src: Iterable[T]) -> Iterable[T]:
    return dict.fromkeys(src).keys()


def unique[T](src: Iterable[T]) -> Generator[T, None, None]:
    emerged = set()
    for elem in src:
        if elem in emerged:
            continue
        emerged.add(elem)
        yield elem


def repeat[T](f: Callable[[], T], times: int) -> Generator[T, None, None]:
    return (f() for _ in range(times))


def skip_last[T](values: Iterable[T]) -> Iterator[T]:
    return chain.from_iterable(islice(p, 1) for p in pairwise(values))


class CounterIterator[T](Iterator[T]):
    def __init__(self, iterator: Iterator[T]):
        self.__underlying = iterator
        self.__count = 0

    @property
    def count(self) -> int:
        return self.__count

    def __next__(self) -> T:
        val = next(self.__underlying)
        self.__count += 1
        return val


if __name__ == '__main__':

    ci: CounterIterator[int] = CounterIterator(i for i in range(100))
    for i in ci:
        print(f'value: {i}')
    print(f'count: {ci.count}')

    def my_gen(limit: int = 10) -> Generator[int, int, None]:
        i = 0
        while i <= limit:
            r = yield i
            print(f'recved {r}')
            i = i+1 if r is None else r

    g = my_gen(10)
    for i in islice(g, 5):
        print(f'a: {i}')

    g.send(9)

    for i in g:
        print(f'b: {i}')

    sys.exit()

    import pandas as pd

    print(group_by_key(lambda x: x % 3)(range(10)))
    print(group_by_key(lambda x: str(x % 3))(range(10)))

    l = [1,[2,4,1,'hoge',[1],2,[5,100,9],3],3,[1,4,3]]
    print(pd.Series(l).explode().explode().tolist())

    print(set(flatten(l)))
    print(list(uniq(flatten(l))))
    print(pd.Series(l).explode().explode().unique().tolist())

    xs = tuple(repeat(lambda: random.uniform(0, 100), 1000000))
    print(timeit.timeit('minmax_(xs)', number=10, globals=globals()))
    print(timeit.timeit('minmax(xs)', number=10, globals=globals()))
    print(timeit.timeit('minmax1(xs)', number=10, globals=globals()))


    argapplier = lambda arg: lambda f:  f(arg)
    a, b = map(argapplier(xs), (min, max))
    print((a, b))