#!/usr/bin/env python3

import string
import sys
from functools import reduce
from random import choice, sample, choices

ALPHAMERICS = [string.digits, string.ascii_uppercase, string.ascii_lowercase]

def main():
    print('パスワードの長さは? [20]: ', end='')
    size = int(input() or 20)

    print('追加の文字は?: ', end='')
    letters = input()

    print()
    try:
        for password in generate_passwords(size, additional_letters=letters):
            print(password)
    except Exception as e:
        print(e, file=sys.stderr)

    print()
    print('\n続行するには、Enter キーを押してください...:', end='')
    input()


def generate_passwords(length: int = 20, n: int = 10, additional_letters: str | None = None) -> list[str]:
    populations = (ALPHAMERICS + [additional_letters]) if additional_letters else ALPHAMERICS

    if length < len(populations):
        raise Exception('Too short password length')

    letters = reduce(lambda acc, p: acc + p, populations)
    return [passwd(length, populations, letters) for _ in range(n)]


def passwd(length: int, populations: list[str], using_letters: str) -> str:
    pickups = [choice(p) for p in populations]
    tail_letters = choices(using_letters, k=length - len(populations))
    return ''.join(sample(pickups + tail_letters, k=length))


if __name__ == '__main__':
    main()
