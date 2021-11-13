import argparse
import itertools
import sys
from random import choices

import numpy as np

from src.sampling_simulator_3 import simulate
from src.sampling_simulator_util import array, decompose3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('p1', type=float)
    parser.add_argument('p2', type=float)
    parser.add_argument('p3', type=float)
    parser.add_argument('p12', type=float)
    parser.add_argument('p13', type=float)
    parser.add_argument('p23', type=float)
    parser.add_argument('p123', type=float, nargs='?')
    parser.add_argument('-n', '--total-size', type=int, default=1000000, help='(default: 1000000)')
    args = parser.parse_args()

    if args.p123 is None:
        p1, p2, p3, p12, p13, p23 = args.p1, args.p2, args.p3, args.p12, args.p13, args.p23
        p123 = round(1 - sum((p1, p2, p3, p12, p13, p23)), 9)
        if p12 < 0:
            print('the sum of params exceeds 1', file=sys.stderr)
            exit(-1)
    else:
        orig = array(args.p1, args.p2, args.p3, args.p12, args.p13, args.p23, args.p123)
        p1, p2, p3, p12, p13, p23, p123 = orig / orig.sum()

    print(f'p1: {p1}, p2: {p2}, p3: {p3}, p12: {p12}, p13: {p13}, p23: {p23}, p123: {p123}')

    set1, set2, set3 = generate_testsets(p1, p2, p3, p12, p13, p23, p123, args.total_size)

    run_simulations(set1, set2, set3)


def generate_testsets(p1, p2, p3, p12, p13, p23, p123, total_size):
    lists = ([], [], [])

    for i in range(total_size):
        for targets in choices(([0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]), (p1, p2, p3, p12, p13, p23, p123)):
            for target in targets:
                lists[target].append(i)

    return list(map(set, lists))


def run_simulations(set1, set2, set3):
    n = decompose3(set1, set2, set3)

    # for sampling_rate1, sampling_rate2 in combinations_with_replacement(np.arange(0.1, 1, 0.1), 2):
    for sampling_rate1, sampling_rate2, sampling_rate3 in itertools.product(np.arange(0.1, 1, 0.2), np.arange(0.1, 1, 0.2), np.arange(0.1, 1, 0.2)):
        print('========================================================================================================')
        print(f'sampling rate: {round(sampling_rate1, 9)} {round(sampling_rate2, 9)} {round(sampling_rate3, 9)}')
        simulate(set1, set2, set3, n, sampling_rate1, sampling_rate2, sampling_rate3)


if __name__ == '__main__':
    main()
