
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from random import sample
from typing import TypeVar

import matplotlib.pyplot as plt
import numpy as np

from src.sampling_driver import generate_testsets
from src.sampling_simulator import do_correction
from src.sampling_simulator_util import array, Cardinality3
from src.sampling_simulator_util import decompose3


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

    c3 = decompose3(set1, set2, set3)

    print([c3.size1, c3.size2, c3.size3, c3.size12, c3.size13, c3.size23, c3.size123])

    simulate(set1, set2, set3, 1000)


T = TypeVar('T')


def sample_at_rate(population: set[T], rate: float):
    return sample(list(population), round(len(population) * rate))


def pickup_cross_region_elements(set1: set[T], set2: set[T], set3: set[T], sampling_rate: float = 0.1) -> Cardinality3:
    sample1, sample2, sample3 = (sample_at_rate(s, sampling_rate) for s in (set1, set2, set3))
    return decompose3(sample1, sample2, sample3)


def f(args):
    return pickup_cross_region_elements(args[0], args[1], args[2], args[3])


def print_summary(data):
    print(f'mean = {data.mean()}, stddev = {data.std(ddof=1)}, 2.5%ile = {np.percentile(data, 2.5)}, 1Q = {np.percentile(data, 25)},'
          f' Median = {np.percentile(data, 50)}, 3Q = {np.percentile(data, 75)}, 97.5%ile = {np.percentile(data, 97.5)}')


def simulate(set1, set2, set3, epoch: int):
    sampling_rate = 0.1
    executor = ProcessPoolExecutor(max_workers=16)

    results = tuple(executor.map(f, [(set1, set2, set3, sampling_rate) for _ in range(epoch)]))

    corrected = [do_correction(r, sampling_rate, sampling_rate, sampling_rate) for r in results]

    cross12 = np.array([r.size12 for r in results])
    cross12_corrected = np.array([r.size12 for r in corrected])
    print('12')
    print_summary(cross12)
    print_summary(cross12_corrected)

    cross13 = np.array([r.size13 for r in results])
    cross13_corrected = np.array([r.size13 for r in corrected])
    print('13')
    print_summary(cross13)
    print_summary(cross13_corrected)

    cross23 = np.array([r.size23 for r in results])
    cross23_corrected = np.array([r.size23 for r in corrected])
    print('23')
    print_summary(cross23)
    print_summary(cross23_corrected)

    cross123 = np.array([r.size123 for r in results])
    cross123_corrected = np.array([r.size123 for r in corrected])
    print('123')
    print_summary(cross123)
    print_summary(cross123_corrected)

    plt.hist(cross123)
    plt.show()


if __name__ == '__main__':
    main()
