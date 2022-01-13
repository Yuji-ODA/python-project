#!/usr/bin/env python3

import shutil
import string
from concurrent.futures import ProcessPoolExecutor
from functools import reduce
from itertools import combinations, chain, islice, count
from operator import itemgetter, lt, gt
from os import makedirs
from random import choices, random

import numpy as np


def main():
    p1, p2, p3, p12, p13, p23, p123 = 0.25, 0.35, 0.25, 0.06, 0.03, 0.04, 0.02
    sampling_rate = 0.1
    unique_users = 3000000
    base_dir = 'output'

    splits = 16
    max_workers = 8
    probs = (p1, p2, p3, p12, p13, p23, p123)
    generate_userlists(probs, sampling_rate, unique_users, splits, base_dir, max_workers)


def generate_userlists(probs, sampling_rate, unique_users, splits, base_dir, max_workers):
    makedirs(base_dir, exist_ok=True)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for task_id in range(splits):
            executor.submit(save_guid_sets, probs, unique_users // splits, task_id, base_dir)

    with ProcessPoolExecutor(max_workers=3) as executor:
        for i in range(1, 4):
            executor.submit(merge_work_files, i, splits, base_dir)

    with ProcessPoolExecutor(max_workers=3) as executor:
        for i in range(1, 4):
            executor.submit(sample_file, f'{base_dir}/list{i}.tsv', f'{base_dir}/sample{i}.tsv', sampling_rate)

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

    for i, userlist in enumerate(userlists):
        with open(f'{work_dir}/list{i+1}.tsv', 'w') as dest:
            for guid, score in userlist:
                print('\t'.join((guid, str(score))), file=dest)


def merge_work_files(k, splits, base_dir):
    work_dir = f'{base_dir}/work'
    dest_file = f'{base_dir}/list{k}.tsv'

    sources = [open(f'{work_dir}/t{task_id}/list{k}.tsv') for task_id in range(1, splits)]

    with open(dest_file, 'w') as dest:
        merge_file(sources, dest, lambda line: float(line.split('\t')[1]), reverse=True)

    for src in sources:
        src.close()


def sample_file(src_file, dest_file, sampling_rate):
    with open(src_file) as src, open(dest_file, 'w') as sample:
        for line in src:
            if random() < sampling_rate:
                sample.write(line)


def merge_file(sources, dest, key, reverse=False):

    def read_next(src):
        try:
            line = next(src).rstrip('\r\n')
            return line, key(line)
        except StopIteration:
            return None

    selection_func = min_with_index if reverse else max_with_index
    buf = [read_next(src) for src in sources]

    while any(buf):
        index, value = selection_func(buf, itemgetter(1))
        print(value[0], file=dest)
        buf[index] = read_next(sources[index])


def guid_seq(times=None):
    return (generate_guid() for _ in islice(count(), times))


def generate_guid():
    return ''.join(choices(string.ascii_uppercase + string.digits, k=26))


def powerset(elements):
    return chain.from_iterable(combinations(elements, r) for r in range(len(elements)+1))


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


def max_with_index(seq, key=lambda x: x):
    return reduce(build_reducer(gt, key), enumerate(seq), (None,))[0]


def min_with_index(seq, key=lambda x: x):
    return reduce(build_reducer(lt, key), enumerate(seq), (None,))[0]


if __name__ == '__main__':
    main()
