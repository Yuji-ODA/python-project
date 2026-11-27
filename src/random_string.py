#!/usr/bin/env python3

import string
import sys
from functools import reduce
from random import choice, sample, choices
from typing import Generator

ALPHAMERICS = [string.digits, string.ascii_uppercase, string.ascii_lowercase]

def generate_passwd(length: int = 20, n: int = 10, additional_letters: str | None = None) -> Generator[str, None, None]:
    populations = (ALPHAMERICS + [additional_letters]) if additional_letters else ALPHAMERICS

    if length < len(populations):
        raise Exception('Too short password length')

    letter_population = reduce(lambda acc, p: acc + p, populations)
    for _ in range(n):
        pickups = [choice(p) for p in populations]
        tail_letters = choices(letter_population, k=length - len(populations))
        yield ''.join(sample(pickups + tail_letters, k=length))


if __name__ == '__main__':
    print('パスワードの長さは? [20]: ', end='')
    size = int(input() or 20)

    print('追加の文字は?: ', end='')
    letters = input()

    try:
        for password in generate_passwd(size, additional_letters=letters):
            print(password)
    except Exception as e:
        print(e, file=sys.stderr)

    print()
    print('\n続行するには、Enter キーを押してください...:', end='')
    input()
