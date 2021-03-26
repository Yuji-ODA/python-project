from contextlib import contextmanager

import requests


@contextmanager
def open_text_stream(url: str):
    with requests.get(url, stream=True) as res:
        yield res.iter_lines(decode_unicode=True)


if __name__ == '__main__':
    url = 'https://jjwd.info/api/v2/stations/search?pref_ja=埼玉&address=越谷'
    with open_text_stream(url) as f:
        for i, line in enumerate(f):
            print(i, line.rstrip())
