#!/usr/bin/env python3

import random

NUMBER = tuple(str(i) for i in range(10))
ALPHAMERIC = tuple(list(NUMBER) + [chr(ord('A') + i) for i in range(26)] + [chr(ord('a') + i) for i in range(26)] + ['-'])
ALPHAMERIC_AND_SYMBOL = tuple(ALPHAMERIC + ('$', '#', '=', '?', '_', '[', ']', '/'))


def random_string(length, letters=ALPHAMERIC):
  return ''.join([letters[random.randint(0, len(letters) - 1)] for _ in range(length)])


if __name__ == '__main__':
    import sys

    length = nt(sys.argv[1]) if 1 < len(sys.argv) else 10

    print(random_string(length, ALPHAMERIC))
