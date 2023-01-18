import itertools
from collections import defaultdict
from functools import reduce
from typing import List, TypeVar, Callable, Generator, Mapping
from urllib.parse import urlparse, ParseResult, urlunparse, urlencode

T = TypeVar('T')
QueryMapping = Mapping[str, List[str]]


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
        query_mapping = parse_query(self._parse_result.query)
        query_mapping[name].extend(values)
        new_query = '&'.join(itertools.chain.from_iterable(expand_mapping(lambda n, v: f'{n}={v}', query_mapping)))
        return self.from_parse_result(self._parse_result._replace(query=new_query))

    def build(self) -> str:
        query_mapping = parse_query(self._parse_result.query)
        queries = expand_mapping(lambda n, v: (n, v), query_mapping)
        encoded_query = urlencode(list(itertools.chain.from_iterable(queries)))
        return urlunparse(self._parse_result._replace(query=encoded_query))


def parse_query(qs: str) -> QueryMapping:
    store = defaultdict(list)
    for query in qs.split('&'):
        if len(query) == 0:
            continue
        k, v = query.split('=')
        store[k].append(v)
    return store


def expand_mapping(f: Callable[[str, str], T], mapping: QueryMapping) \
        -> Generator[Generator[T, None, None], None, None]:

    return ((f(name, value) for value in values) for name, values in mapping.items())


if __name__ == '__main__':

    url = UrlBuilder.from_url_string('https://www.yahoo.co.jp/')\
        .query_param('key1', 'key1-value1', 'key1-value2')\
        .query_param('key2', 'key2-value1', 'key2-value2')\
        .path_segment('l1', 'l2', 'l3')\
        .build()

    print(url)
