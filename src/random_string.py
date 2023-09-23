#!/usr/bin/env python3

import sys
import random
import string

NUMBERS = string.digits
ALPHAMERIC = NUMBERS + string.ascii_letters
ALPHAMERIC_AND_SYMBOLS = ALPHAMERIC + '-$#=?_[]/'


def main():
    length = int(sys.argv[1]) if 1 < len(sys.argv) else 16
    print(random_string(length, ALPHAMERIC))


def random_string(size, letters=ALPHAMERIC):
    return ''.join(random.sample(letters, size))


if __name__ == '__main__':
    main()
