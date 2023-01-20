from functools import reduce
from itertools import chain
from typing import List, TypeVar, Callable, Iterator, MutableMapping
from urllib.parse import SplitResult, urlencode, urlsplit, parse_qs, quote

T = TypeVar('T')
QueryMapping = MutableMapping[str, List[str]]


class UrlBuilder:
    def __init__(self, split_result: SplitResult):
        self._p = split_result
        self._encode: bool = False

    @classmethod
    def from_url_string(cls, url_str: str):
        return cls(urlsplit(url_str))

    def path_segment(self, *path: str) -> 'UrlBuilder':
        new_path = reduce(lambda acc, e: f'{acc}/{e}', path, self._p.path.rstrip('/'))
        self._p = self._p._replace(path=new_path)
        return self

    def query_param(self, name: str, *values: str) -> 'UrlBuilder':
        query_mapping = parse_qs(self._p.query)
        add_values(query_mapping, name, *values)
        queries = expand_mapping(lambda n, v: f'{n}={v}', query_mapping)
        self._p = self._p._replace(query='&'.join(queries))
        return self

    def encode(self) -> 'UrlBuilder':
        self._encode = True
        return self

    def fragment(self, fragment: str):
        self._p = self._p._replace(fragment=fragment)
        return self

    def build(self) -> str:
        if not self._encode:
            return self._p.geturl()

        query_mapping = parse_qs(self._p.query)
        encoded_query = urlencode(list(expand_mapping(lambda n, v: (n, v), query_mapping)))
        return self._p._replace(query=encoded_query).\
            _replace(path=quote(self._p.path)). \
            _replace(fragment=quote(self._p.fragment)). \
            geturl()


def expand_mapping(f: Callable[[str, str], T], mapping: QueryMapping) -> Iterator[T]:
    def mapper(item):
        name, values = item
        return map(lambda value: f(name, value), values)

    return chain.from_iterable(map(mapper, mapping.items()))


def add_values(mapping: QueryMapping, name: str, *values: str):
    if name not in mapping:
        mapping[name] = []
    mapping[name].extend(values)


if __name__ == '__main__':

    url = UrlBuilder.from_url_string('https://www.yahoo.co.jp/')\
        .query_param('key1', 'key1-value1', 'key1-value2')\
        .query_param('キー2', 'キー２-値１')\
        .path_segment('next', 'bottom.html')\
        .fragment('here')\
        .encode()\
        .build()

    print(url)
