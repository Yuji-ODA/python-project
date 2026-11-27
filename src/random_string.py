#!/usr/bin/env python3

import string
import sys
from functools import reduce
from operator import add
from random import choice, sample, choices

ALPHAMERICS = [string.digits, string.ascii_uppercase, string.ascii_lowercase]
ALPHAMERIC_AND_SYMBOLS = ALPHAMERICS + ['/*-+.,!#$%&()~|_']

def generate_passwd(length: int = 20, additional_letters: list[str] | None = None):
    populations = (ALPHAMERICS + additional_letters) if additional_letters else ALPHAMERICS

    letters = [choice(p) for p in populations] + choices(reduce(add, populations), k=length - len(populations))

    print()
    for _ in range(10):
        print(''.join(sample(letters, length)))


if __name__ == '__main__':
    print('length? [20]: ', end='')
    l = input()
    size = int(l) if l else 20
    if size < 4:
        sys.exit('Too few arguments')

    print('letters?: ', end='')
    letters = list(input())

    generate_passwd(size, letters)

    print('\n続行するには、Enter キーを押してください...:', end='')
    input()
