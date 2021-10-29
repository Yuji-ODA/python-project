
from functools import reduce, wraps
from typing import Callable, Any, Iterable, Union, TextIO, ContextManager


def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda acc, func: lambda x: func(acc(x)), functions)


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda acc, func: lambda x: acc(func(x)), functions)


print(pipe(lambda x: x*2, lambda x: x+2)(10))
print(compose(lambda x: x*2, lambda x: x+2)(10))


def from_stream_supplier(func):
    @wraps(func)
    def _wrapper(src: Union[str, Iterable[str], Callable[[], ContextManager[TextIO]]], *args, **kwargs):
        if isinstance(src, str):
            open_args = {'file': src, 'encoding': kwargs.pop('encoding') if 'encoding' in kwargs else 'utf-8'}
            with open(**open_args) as fin:
                return func(fin, *args, **kwargs)
        elif hasattr(src, '__iter__'):
            return func(src, *args, **kwargs)
        elif callable(src):
            with src() as fin:
                return func(fin, *args, **kwargs)
        else:
            print(f'src is not supported type: {type(src)}')
    return _wrapper


@from_stream_supplier
def print_elements(stream):
    for line in stream:
        print(line.rstrip())


print_elements('logger.py', encoding='utf-8')
print_elements(iter('logger.py'))
print_elements(lambda: open('logger_injector.py'))
print_elements(1)
