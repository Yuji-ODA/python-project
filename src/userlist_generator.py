#!/usr/bin/env python3

import argparse
import multiprocessing
import shutil
import string
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import reduce
from itertools import combinations, chain, islice, count
from operator import itemgetter, lt, gt
from os import makedirs
from random import choices, sample

import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('p1', type=float)
    parser.add_argument('p2', type=float)
    parser.add_argument('p3', type=float)
    parser.add_argument('p12', type=float)
    parser.add_argument('p13', type=float)
    parser.add_argument('p23', type=float)
    parser.add_argument('p123', type=float, nargs='?')
    parser.add_argument('-u', '--users', type=int, default=3000000, help='size of unique users (default: 3000000)')
    parser.add_argument('-r', '--sampling-rate', type=float, default=0.1, help='sampling rate (default: 0.1)')
    parser.add_argument('-d', '--output-dir', type=str, default='output',
                        help='dir for output results (default: ./output)')
    parser.add_argument('-s', '--splits', type=int, default=multiprocessing.cpu_count(), help='(default: cpu count)')
    parser.add_argument('-n', '--max-workers', type=int, default=multiprocessing.cpu_count(),
                        help='(default: cpu count)')
    args = parser.parse_args()

    if args.p123 is None:
        p1, p2, p3, p12, p13, p23 = args.p1, args.p2, args.p3, args.p12, args.p13, args.p23
        p123 = round(1 - sum((p1, p2, p3, p12, p13, p23)), 9)
        if p12 < 0:
            print('the sum of params exceeds 1', file=sys.stderr)
            exit(-1)
    else:
        orig = np.array((args.p1, args.p2, args.p3, args.p12, args.p13, args.p23, args.p123))
        p1, p2, p3, p12, p13, p23, p123 = orig / orig.sum()

    print(f'p1={p1}, p2={p2}, p3={p3}, p12={p12}, p13={p13}, p23={p23}, p123={p123}')
    print(f'users={args.users}, sampling rate={args.sampling_rate}, output dir={args.output_dir}')
    print(f'splits={args.splits}, max workers={args.max_workers}')

    probs = (p1, p2, p3, p12, p13, p23, p123)
    generate_userlists(probs, args.users, args.sampling_rate, args.output_dir, args.splits, args.max_workers)


def generate_userlists(probs, unique_users, sampling_rate, base_dir, splits, max_workers):
    makedirs(base_dir, exist_ok=True)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for task_id in range(splits):
            executor.submit(save_guid_sets, probs, unique_users // splits, task_id, base_dir)

    with ProcessPoolExecutor(max_workers=3) as executor:
        for i in range(1, 4):
            executor.submit(merge_and_sample, i, sampling_rate, base_dir, splits)

    shutil.rmtree(f'{base_dir}/work')


def save_guid_sets(probs, unique_users, task_id, base_dir):
    work_dir = f'{base_dir}/work/t{task_id}'
    makedirs(work_dir, exist_ok=True)

    destinations = tuple(islice(powerset(range(3)), 1, None))
    buf = [{} for _ in range(3)]
    for guid in guid_seq(unique_users):
        for indices in choices(destinations, probs):
            for index in indices:
                buf[index][guid] = round(np.random.beta(1, 3), 3)

    userlists = [sorted(userlist.items(), key=itemgetter(1), reverse=True) for userlist in buf]

    for i, userlist in enumerate(userlists, start=1):
        with open(f'{work_dir}/list{i}.tsv', 'w') as dest:
            for guid, score in userlist:
                print('\t'.join((guid, str(score))), file=dest)


def merge_and_sample(k, sampling_rate, base_dir, splits):
    line_count = merge_work_files(k, splits, base_dir)
    sample_from_file(f'{base_dir}/list{k}.tsv', f'{base_dir}/sample{k}.tsv', sampling_rate, line_count)


def merge_work_files(k, splits, base_dir) -> int:
    work_dir = f'{base_dir}/work'
    input_files = [f'{work_dir}/t{task_id}/list{k}.tsv'for task_id in range(splits)]
    dest_file = f'{base_dir}/list{k}.tsv'

    return merge_file(input_files, dest_file, lambda line: float(line.split('\t')[1]), reverse=True)


def sample_from_file(src_file, dest_file, sampling_rate, total_count):
    sample_count = round(sampling_rate * total_count)
    sample_indices = set(sample(range(sample_count), sample_count))
    with open(src_file) as src, open(dest_file, 'w') as dest:
        for i, line in enumerate(src):
            if i in sample_indices:
                dest.write(line)


def merge_file(input_files, dest_file, key, reverse=False) -> int:
    sources = [open(file) for file in input_files]

    def read_next(src):
        try:
            line = next(src).rstrip('\r\n')
            return line, key(line)
        except StopIteration:
            return None

    selection_func = max_with_index if reverse else min_with_index
    buf = [read_next(src) for src in sources]

    total_count = 0
    with open(dest_file, 'w') as out:
        while any(buf):
            index, value = selection_func(buf, itemgetter(1))
            print(value[0], file=out)
            total_count += 1
            buf[index] = read_next(sources[index])

    for source in sources:
        source.close()

    return total_count


def max_with_index(seq, key=lambda x: x):
    return reduce(build_reducer(gt, key), enumerate(seq), (None,))[0]


def min_with_index(seq, key=lambda x: x):
    return reduce(build_reducer(lt, key), enumerate(seq), (None,))[0]


def build_reducer(comparator, key):
    def reducer(acc, elem):
        if acc[0] is None:
            return elem, None if elem[1] is None else key(elem[1])

        if elem[1] is not None:
            value = key(elem[1])
            if acc[1] is None or comparator(value, acc[1]):
                return elem, value

        return acc

    return reducer


def guid_seq(times=None):
    return (generate_guid() for _ in islice(count(), times))


def generate_guid():
    return ''.join(choices(string.ascii_uppercase + string.digits, k=26))


def powerset(elements):
    return chain.from_iterable(combinations(elements, r) for r in range(len(elements)+1))


if __name__ == '__main__':
    main()
