from random import sample

import numpy as np

set1 = set(range(0, 250000))
set2 = set(range(200000, 500000))

intersect_len = len(set(set1).intersection(set2))
union_len = len(set(set1).union(set2))

p1 = (len(set1) - intersect_len) / union_len
p2 = (len(set2) - intersect_len) / union_len
p12 = intersect_len / union_len

print(f'p1: {p1}, p2: {p2}, p12: {p12}')

for sampling_rate in np.arange(0.1, 1, 0.1):
    print('==============================================================')
    print(f'sampling rate: {sampling_rate}')

    sample1 = set(sample(set1, int(len(set1) * sampling_rate)))
    sample2 = set(sample(set2, int(len(set2) * sampling_rate)))

    sample_intersection_size = len(sample1.intersection(sample2))
    sample_union_size = len(sample1.union(sample2))

    print(f'expected: {p12 * sample_union_size}, proportion: {p12}')
    print(f'actual: {sample_intersection_size}, proportion: {sample_intersection_size / sample_union_size}')
    print(f'estimated: {p12 * sample_union_size * sampling_rate}, proportion: {p12 * sampling_rate}')
