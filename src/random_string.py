#!/usr/bin/env python3

import string
import sys
from functools import reduce
from random import choice, sample, choices

ALPHAMERICS = [string.digits, string.ascii_uppercase, string.ascii_lowercase]

def generate_passwd(length: int = 20, n: int = 10, additional_letters: list[str] | None = None) -> list[str]:
    populations = (ALPHAMERICS + additional_letters) if additional_letters else ALPHAMERICS

    letter_population = [choice(p) for p in populations] + choices(reduce(lambda acc, p: acc + p, populations), k=length - len(populations))
    return [''.join(sample(letter_population, length)) for _ in range(10)]


if __name__ == '__main__':
    print('パスワードの長さは? [20]: ', end='')
    l = input()
    size = int(l) if l else 20
    if size < 4:
        sys.exit('Too few arguments')

    print('追加の文字は?: ', end='')
    letters = list(input())

    print()
    for p in generate_passwd(size, additional_letters=letters):
        print(p)

    print('\n続行するには、Enter キーを押してください...:', end='')
    input()
