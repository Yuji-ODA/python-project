
from functools import reduce, wraps
from typing import Callable, Any, Iterable, Union


def pipe(*functions: Callable[[Any], Any]):
    return reduce(lambda acc, func: lambda x: func(acc(x)), functions)


def compose(*functions: Callable[[Any], Any]):
    return reduce(lambda acc, func: lambda x: acc(func(x)), functions)


print(pipe(lambda x: x*2, lambda x: x+2)(10))
print(compose(lambda x: x*2, lambda x: x+2)(10))


def from_file(func):
    @wraps(func)
    def _wrapper(src: Union[str, Iterable[str]], *args, **kwargs):
        if isinstance(src, str):
            open_args = {'file': src, 'encoding': kwargs.pop('encoding') if 'encoding' in kwargs else 'utf-8'}
            with open(**open_args) as fin:
                return func(fin, *args, **kwargs)
        else:
            return func(src, *args, **kwargs)
    return _wrapper


@from_file
def print_lines(stream: Iterable[str]):
    for line in stream:
        print(line.rstrip())


print_lines('logger.py', encoding='utf-8')
print_lines(iter('logger.py'))
