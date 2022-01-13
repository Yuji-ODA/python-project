#!/usr/bin/env python3

import os.path
import shutil
import string
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations, chain, islice, count
from operator import itemgetter
from os import makedirs
from random import choices, random

import numpy as np


def main():
    p1, p2, p3, p12, p13, p23, p123 = 0.25, 0.35, 0.25, 0.06, 0.03, 0.04, 0.02
    sampling_rate = 0.1
    unique_users = 300000
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
    work_file = f'{work_dir}/tmp-list{k}'
    dest_file = f'{base_dir}/list{k}.tsv'

    if os.path.exists(f'{work_dir}/t0/list{k}.tsv'):
        shutil.move(f'{work_dir}/t0/list{k}.tsv', dest_file)

    for task_id in range(1, splits):
        task_dir = f'{work_dir}/t{task_id}'
        with open(dest_file) as src1, open(f'{task_dir}/list{k}.tsv') as src2, open(work_file, 'w') as work:
            merge_file(src1, src2, work, lambda line: float(line.split('\t')[1]), reverse=True)

        shutil.move(work_file, dest_file)


def sample_file(src_file, dest_file, sampling_rate):
    with open(src_file) as src, open(dest_file, 'w') as sample:
        for line in src:
            if random() < sampling_rate:
                sample.write(line)


def merge_file(src1, src2, dest, key, reverse=False):

    def read_next(src):
        try:
            return next(src)
        except StopIteration:
            return None

    line1, line2 = read_next(src1), read_next(src2)

    while any((line1, line2)):
        if line2 is None or (key(line1.rstrip('\r\n')) <= key(line2.rstrip('\r\n'))) ^ reverse:
            dest.write(line1)
            if line1 is not None:
                line1 = read_next(src1)
        else:
            dest.write(line2)
            if line2 is not None:
                line2 = read_next(src2)


def guid_seq(times=None):
    return (generate_guid() for _ in islice(count(), times))


def generate_guid():
    return ''.join(choices(string.ascii_uppercase + string.digits, k=26))


def powerset(elements):
    return chain.from_iterable(combinations(elements, r) for r in range(len(elements)+1))


if __name__ == '__main__':
    main()
