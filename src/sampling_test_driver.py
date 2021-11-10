from random import sample

import numpy as np

set1 = set(range(0, 250000))
set2 = set(range(200000, 500000))

set1_size = len(set1)
set2_size = len(set2)

intersect = set(set1).intersection(set2)
intersect_size = len(intersect)
union = set(set1).union(set2)
union_size = len(union)

p1 = (len(set1) - intersect_size) / union_size
p2 = (len(set2) - intersect_size) / union_size
p12 = intersect_size / union_size

print(f'p1: {p1}, p2: {p2}, p12: {p12}')

for sampling_rate in np.arange(0.1, 1, 0.1):
    print('==============================================================')
    print(f'sampling rate: {sampling_rate}')

    sample1 = set(sample(list(set1), int(len(set1) * sampling_rate)))
    sample2 = set(sample(list(set2), int(len(set2) * sampling_rate)))

    sample_intersection = sample1.intersection(sample2)
    sample_union_size_actual = len(sample1.union(sample2))
    n12_actual = len(sample_intersection)
    p12_actual = n12_actual / sample_union_size_actual

    n12_expected = sampling_rate * intersect_size
    sample_union_size_expected = sampling_rate * union_size
    p12_expected = n12_expected / sample_union_size_expected

    n12_computed = (sampling_rate ** 2) * intersect_size
    sample_union_size_computed = sampling_rate * (set1_size + set2_size - n12_computed)
    p12_computed = n12_computed / sample_union_size_computed

    n12_corrected = n12_actual / sampling_rate
    p12_corrected = n12_corrected / sample_union_size_actual

    print(f'expected: {n12_expected}, proportion: {p12_expected}')
    print(f'actual: {n12_actual}, proportion: {p12_actual}')
    print(f'computed: {n12_computed}, proportion: {p12_computed}')
    print(f'corrected: {n12_corrected}, proportion: {p12_corrected}')
