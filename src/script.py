
from functools import reduce, wraps
from typing import Callable, Any, Iterable, Union


def pipe(*functions: Callable[[Any], Any]):
    return reduce(lambda acc, func: lambda x: func(acc(x)), functions)


def compose(*functions: Callable[[Any], Any]):
    return reduce(lambda acc, func: lambda x: acc(func(x)), functions)


print(pipe(lambda x: x*2, lambda x: x+2)(10))
print(compose(lambda x: x*2, lambda x: x+2)(10))


def from_file(encoding: str = 'utf-8'):
    def _decorator(func):
        @wraps(func)
        def _wrapper(src: Union[str, Iterable[str]], *args, **kwargs):
            if isinstance(src, str):
                with open(src, encoding=encoding) as fin:
                    return func(fin, *args, **kwargs)
            else:
                return func(src, *args, **kwargs)
        return _wrapper
    return _decorator


@from_file()
def print_lines(stream: Iterable[str]):
    for line in stream:
        print(line.rstrip())


f = from_file('utf-8')(print_lines)

f('logger.py')
f(iter('logger.py'))
