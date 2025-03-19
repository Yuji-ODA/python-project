
from itertools import groupby
from typing import Iterable, Any, Generator

import pandas as pd


def group_by_key(f):
    return lambda x: {k: tuple(v) for k, v in groupby(sorted(x, key=f), f)}


def flatten(src: Iterable[Any]) -> Generator[Any, None, None]:
    for elem in src:
        if isinstance(elem, Iterable) and not isinstance(elem, str):
            yield from flatten(elem)
        else:
            yield elem

def uniq(src: Iterable[Any]) -> Iterable[Any]:
    return {k: None for k in src}.keys()


if __name__ == '__main__':
    print(group_by_key(lambda x: x % 3)(range(10)))
    print(group_by_key(lambda x: str(x % 3))(range(10)))

    l = [1,[2,4,1,'hoge',[1],2,[5,100,9],3],3,[1,4,3]]
    print(list(flatten(l)))
    print(pd.Series(l).explode().explode().tolist())

    print(set(flatten(l)))
    print(list(uniq(flatten(l))))
    print(pd.Series(l).explode().explode().unique().tolist())
