#!/usr/bin/env python3

from concurrent.futures import ProcessPoolExecutor
from os import makedirs
import string
from itertools import combinations, chain, islice
from random import choices, random

import numpy as np


def main():
    p1, p2, p3, p12, p13, p23, p123 = 0.25, 0.35, 0.25, 0.06, 0.03, 0.04, 0.02
    sampling_rate = 0.1
    unique_users = 30000000
    base_dir = 'output'

    splits = 8
    probs = (p1, p2, p3, p12, p13, p23, p123)
    generate_userlists(probs, sampling_rate, unique_users, splits, base_dir)


def generate_userlists(probs, sampling_rate, unique_users, splits, base_dir):
    makedirs(base_dir, exist_ok=True)

    with ProcessPoolExecutor() as executor:
        for task_id in range(splits):
            executor.submit(save_guid_sets, probs, unique_users // splits, task_id, base_dir)

    with ProcessPoolExecutor() as executor:
        for i in range(1, 4):
            executor.submit(merge_work_files, i, splits, sampling_rate, base_dir)


def save_guid_sets(probs, unique_users, task_id, base_dir):
    work_dir = f'{base_dir}/t{task_id}'
    makedirs(work_dir, exist_ok=True)
    with open(f'{work_dir}/list1.tsv', 'w') as list1, open(f'{work_dir}/list2.tsv', 'w') as list2, \
            open(f'{work_dir}/list3.tsv', 'w') as list3:
        lists = tuple(islice(powerset(list1, list2, list3), 1, None))
        for _ in range(unique_users):
            guid = generate_guid()
            for targets in choices(lists, probs):
                for target in targets:
                    print('\t'.join((guid, str(round(np.random.beta(1, 3), 3)))), file=target)


def merge_work_files(k, splits, sampling_rate, base_dir):
    with open(f'{base_dir}/list{k}.tsv', 'w') as dest, open(f'{base_dir}/sample{k}.tsv', 'w') as sample:
        for task_id in range(splits):
            work_dir = f'{base_dir}/t{task_id}'
            with open(f'{work_dir}/list{k}.tsv') as src:
                for line in src:
                    dest.write(line)
                    if random() < sampling_rate:
                        sample.write(line)


def generate_guid():
    return ''.join(choices(string.ascii_uppercase + string.digits, k=26))


def powerset(*elements):
    return chain.from_iterable(combinations(elements, r) for r in range(len(elements)+1))


if __name__ == '__main__':
    main()
