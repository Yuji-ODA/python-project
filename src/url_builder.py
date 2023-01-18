import itertools
from functools import reduce
from typing import List, TypeVar, Callable, Iterator, MutableMapping
from urllib.parse import urlparse, ParseResult, urlunparse, urlencode, parse_qs

T = TypeVar('T')
QueryMapping = MutableMapping[str, List[str]]


class UrlBuilder:
    def __init__(self, parse_result: ParseResult):
        self._parse_result = parse_result

    @classmethod
    def from_url_string(cls, url_str: str):
        return cls(urlparse(url_str))

    @classmethod
    def from_parse_result(cls, parse_result: ParseResult):
        return cls(parse_result)

    def path_segment(self, *path: str) -> 'UrlBuilder':
        new_path = reduce(lambda acc, e: f'{acc}/{e}', path, self._parse_result.path.rstrip('/'))
        return self.from_parse_result(self._parse_result._replace(path=new_path))

    def query_param(self, name: str, *values: str) -> 'UrlBuilder':
        query_mapping = parse_qs(self._parse_result.query)
        add_values(query_mapping, name, *values)
        new_query = '&'.join(expand_mapping(lambda n, v: f'{n}={v}', query_mapping))
        return self.from_parse_result(self._parse_result._replace(query=new_query))

    def build(self) -> str:
        query_mapping = parse_qs(self._parse_result.query)
        encoded_query = urlencode(list(expand_mapping(lambda n, v: (n, v), query_mapping)))
        return urlunparse(self._parse_result._replace(query=encoded_query))


def expand_mapping(f: Callable[[str, str], T], mapping: QueryMapping) -> Iterator[T]:
    return itertools.chain.from_iterable((f(name, value) for value in values) for name, values in mapping.items())


def add_values(mapping: QueryMapping, name: str, *values: str):
    if name not in mapping:
        mapping[name] = []
    mapping[name].extend(values)


if __name__ == '__main__':

    url = UrlBuilder.from_url_string('https://www.yahoo.co.jp/')\
        .query_param('key1', 'key1-value1', 'key1-value2')\
        .query_param('key2', 'key2-value1', 'key2-value2')\
        .path_segment('l1', 'l2', 'l3')\
        .build()

    print(url)

