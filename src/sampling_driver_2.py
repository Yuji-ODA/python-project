import argparse
import itertools
import sys

import numpy as np

from src.sampling_simulator_2 import simulate
from src.sampling_simulator_util import array, decompose2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('p1', type=float)
    parser.add_argument('p2', type=float)
    parser.add_argument('p12', type=float, nargs='?')
    parser.add_argument('-n', '--total-size', type=int, default=1000000, help='(default: 1000000)')
    args = parser.parse_args()

    if args.p12 is None:
        p1 = args.p1
        p2 = args.p2
        p12 = round(1 - p1 - p2, 9)
        if p12 < 0:
            print('the sum of params should not exceed 1', file=sys.stderr)
            exit(-1)
    else:
        sum_of_fractions = sum((args.p1, args.p12, args.p2))
        p1, p12, p2 = array(args.p1, args.p12, args.p2) / sum_of_fractions

    print(f'p1: {p1}, p12: {p12}, p2: {p2}')

    run_simulations(p1, p12, p2, args.total_size)


def run_simulations(p1, p12, p2, total_size):
    n1, n12, n2 = (round(n) for n in (array(p1, p12, p2) * total_size))
    set1, set2 = set(range(n1 + n12)), set(range(n1, n1 + n12 + n2))

    n = decompose2(set1, set2)

    # for sampling_rate1, sampling_rate2 in combinations_with_replacement(np.arange(0.1, 1, 0.1), 2):
    for sampling_rate1, sampling_rate2 in itertools.product(np.arange(0.1, 1, 0.2), np.arange(0.1, 1, 0.2)):
        print('========================================================================================================'
              '===')
        print(f'sampling rate: {round(sampling_rate1, 9)} {round(sampling_rate2, 9)}')
        simulate(set1, set2, n, sampling_rate1, sampling_rate2)


if __name__ == '__main__':
    main()
