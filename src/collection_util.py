from typing import Iterable, Any, Generator


def distinct(src: Iterable[Any]) -> Iterable[Any]:
    return dict.fromkeys(src).keys()


def distinct_gen(src: Iterable[Any]) -> Generator[Any, None, None]:
    store = set()
    for value in src:
        if value not in store:
            store.add(value)
            yield value


if __name__ == '__main__':
    import random

    orig = random.choices(range(100), k=10000)

    print(orig[:100])

    r: Iterable[int] = distinct(iter(orig))

    print(tuple(r))

    g: Iterable[int] = distinct_gen(iter(orig))

    print(tuple(g))
