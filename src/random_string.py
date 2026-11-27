#!/usr/bin/env python3

import string
import sys
from functools import reduce
from operator import add
from random import choice, sample, choices

ALPHAMERICS = [string.digits, string.ascii_uppercase, string.ascii_lowercase]
ALPHAMERIC_AND_SYMBOLS = ALPHAMERICS + ['/*-+.,!#$%&()~|_']

def main():
    print('length? [20]: ', end='')
    l = input()
    length = int(l) if l else 20
    if length < 4:
        sys.exit('Too few arguments')

    print('letters?: ', end='')
    additional_letters = list(input())
    print(additional_letters)

    populations = ALPHAMERICS + additional_letters if additional_letters else ALPHAMERICS

    letters = [choice(p) for p in populations] + choices(reduce(add, populations), k=length - len(populations))

    for _ in range(10):
        print(''.join(sample(letters, length)))


if __name__ == '__main__':
    main()
