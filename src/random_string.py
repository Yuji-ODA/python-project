#!/usr/bin/env python3

import random
import string

NUMBERS = string.digits
ALPHAMERIC = NUMBERS + string.ascii_letters
ALPHAMERIC_AND_SYMBOLS = ALPHAMERIC + '-$#=?_[]/'


def random_string(length, letters=ALPHAMERIC):
    return ''.join([letters[random.randint(0, len(letters) - 1)] for _ in range(length)])


if __name__ == '__main__':
    import sys

    length = int(sys.argv[1]) if 1 < len(sys.argv) else 16

    print(random_string(length, ALPHAMERIC))
